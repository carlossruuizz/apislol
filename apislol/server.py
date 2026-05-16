__author__ = "Carlos Ruiz"

import socket
import ssl
import threading
import traceback
from typing import Any, Callable

from apislol.request import Request
from apislol.response import Response
from apislol.logger import Logger

HTTP_METHODS = frozenset(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"])
MAX_REQUEST_LINE = 8192
MAX_HEADERS = 100
MAX_BODY_SIZE = 10 * 1024 * 1024

class HttpServer:
    """
    A threaded HTTP/1.1 server.
    Each accepted connection is handled in its own daemon thread.
    Supports optional TLS via ssl_context.
    """

    def __init__(
        self,
        host: str,
        port: int,
        handler: Callable[[Request], Response],
        logger: Logger,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.handler = handler
        self.logger = logger
        self.ssl_context = ssl_context
        self._server_socket: socket.socket | None = None
        self._running = False

    def serve_forever(self) -> None:
        """Starts the server and blocks until interrupted."""
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(128)
        self._running = True

        scheme = "https" if self.ssl_context else "http"
        self.logger.info(f"apislol listening on {scheme}://{self.host}:{self.port}")

        try:
            while self._running:
                try:
                    conn, addr = self._server_socket.accept()
                except OSError:
                    break
                thread = threading.Thread(
                    target=self._handle_connection,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()
        finally:
            self._server_socket.close()

    def shutdown(self) -> None:
        """Signals the server to stop accepting new connections."""
        self._running = False
        if self._server_socket:
            try:
                self._server_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self._server_socket.close()
            except OSError:
                pass

    def _handle_connection(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        if self.ssl_context:
            try:
                conn = self.ssl_context.wrap_socket(conn, server_side=True)
            except ssl.SSLError as exc:
                self.logger.warning(f"TLS handshake failed from {addr[0]}: {exc}")
                conn.close()
                return

        conn.settimeout(30.0)
        try:
            while True:
                request = _parse_request(conn, addr)
                if request is None:
                    break
                try:
                    response = self.handler(request)
                except Exception as exc:
                    self.logger.error(f"Unhandled exception: {_safe_traceback(exc)}")
                    response = Response.error("Internal server error.", status=500)
                _send_response(conn, response)
                connection_header = request.headers.get("connection", "").lower()
                if connection_header == "close" or request.headers.get("http_version", "HTTP/1.0") == "HTTP/1.0":
                    break
        except (ConnectionResetError, BrokenPipeError, TimeoutError):
            pass
        except Exception as exc:
            self.logger.error(f"Connection error from {addr[0]}: {_safe_traceback(exc)}")
        finally:
            try:
                conn.close()
            except OSError:
                pass

def _parse_request(conn: socket.socket, addr: tuple[str, int]) -> Request | None:
    """
    Reads and parses a single HTTP request from the socket.
    Returns None on connection close or parse failure.
    """
    try:
        raw = _read_until(conn, b"\r\n\r\n", MAX_REQUEST_LINE * MAX_HEADERS)
    except (ConnectionResetError, TimeoutError, OSError):
        return None

    if not raw:
        return None

    try:
        separator = b"\r\n\r\n"
        sep_idx = raw.find(separator)
        if sep_idx == -1:
            return None

        header_section = raw[:sep_idx]
        already_buffered = raw[sep_idx + len(separator):]

        lines = header_section.decode("latin-1").split("\r\n")
        if not lines:
            return None

        request_line = lines[0]
        parts = request_line.split(" ")
        if len(parts) != 3:
            return None

        method, raw_path, http_version = parts
        if method not in HTTP_METHODS:
            return None

        path, _, query_string = raw_path.partition("?")

        headers: dict[str, str] = {"http_version": http_version}
        for line in lines[1:]:
            if not line:
                continue
            name, _, value = line.partition(":")
            headers[name.strip()] = value.strip()

        content_length = int(headers.get("Content-Length", headers.get("content-length", 0)))
        content_length = min(content_length, MAX_BODY_SIZE)

        body = already_buffered
        remaining = content_length - len(already_buffered)
        if remaining > 0:
            body += _read_exactly(conn, remaining)
        elif content_length > 0:
            body = body[:content_length]

        return Request(
            method=method,
            path=path,
            headers=headers,
            body=body,
            remote_addr=addr,
            query_string=query_string,
        )
    except Exception:
        return None

def _read_until(conn: socket.socket, delimiter: bytes, max_size: int) -> bytes:
    buf = bytearray()
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            return bytes(buf)
        buf.extend(chunk)
        if delimiter in buf:
            return bytes(buf)
        if len(buf) > max_size:
            raise ValueError("Request headers too large.")

def _read_exactly(conn: socket.socket, length: int) -> bytes:
    buf = bytearray()
    remaining = length
    while remaining > 0:
        chunk = conn.recv(min(remaining, 65536))
        if not chunk:
            break
        buf.extend(chunk)
        remaining -= len(chunk)
    return bytes(buf)

def _send_response(conn: socket.socket, response: Response) -> None:
    content_type = response.headers.pop("Content-Type", None) or response.content_type
    body = response.body

    lines = [
        f"HTTP/1.1 {response.status} {_status_phrase(response.status)}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: keep-alive",
        "X-Powered-By: apislol",
    ]

    for name, value in response.headers.items():
        lines.append(f"{name}: {value}")

    lines.append("")
    lines.append("")

    header_bytes = "\r\n".join(lines).encode("latin-1")
    try:
        conn.sendall(header_bytes + body)
    except (BrokenPipeError, ConnectionResetError):
        pass

def _status_phrase(code: int) -> str:
    phrases = {
        200: "OK", 201: "Created", 204: "No Content",
        301: "Moved Permanently", 302: "Found",
        400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
        404: "Not Found", 405: "Method Not Allowed", 409: "Conflict",
        422: "Unprocessable Entity", 429: "Too Many Requests",
        500: "Internal Server Error", 501: "Not Implemented", 503: "Service Unavailable",
    }
    return phrases.get(code, "Unknown")

def _safe_traceback(exc: Exception) -> str:
    lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    return "".join(lines).strip()

def build_ssl_context(keyfile: str, certfile: str) -> ssl.SSLContext:
    """Creates and returns an SSL context for HTTPS."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=certfile, keyfile=keyfile)
    return ctx