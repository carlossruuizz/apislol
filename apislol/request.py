__author__ = "Carlos Ruiz"

import json
import urllib.parse
from typing import Any

class Request:
    """
    Represents an incoming HTTP request.

    Attributes:
        method      HTTP verb (GET, POST, …)
        path        URL path without query string
        query       Parsed query parameters as a dict
        headers     Dict of header names (lowercased) to values
        body        Raw request body as bytes
        path_params Dict of dynamic path parameters extracted by the router
        client_ip   Remote client IP address
        remote_addr (host, port) tuple of the remote peer
    """

    def __init__(
        self,
        method: str,
        path: str,
        headers: dict[str, str],
        body: bytes,
        remote_addr: tuple[str, int],
        query_string: str = "",
    ) -> None:
        self.method = method.upper()
        self.path = path
        self.headers: dict[str, str] = {k.lower(): v for k, v in headers.items()}
        self.body = body
        self.remote_addr = remote_addr
        self.client_ip: str = self._resolve_client_ip()
        self.query: dict[str, str | list[str]] = self._parse_query(query_string)
        self.path_params: dict[str, str] = {}
        self._json_cache: Any = _MISSING

    def _resolve_client_ip(self) -> str:
        forwarded = self.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = self.headers.get("x-real-ip", "")
        if real_ip:
            return real_ip.strip()
        return self.remote_addr[0]

    def _parse_query(self, query_string: str) -> dict[str, str | list[str]]:
        parsed = urllib.parse.parse_qs(query_string, keep_blank_values=True)
        result: dict[str, str | list[str]] = {}
        for key, values in parsed.items():
            result[key] = values[0] if len(values) == 1 else values
        return result

    def json(self) -> Any:
        """
        Parses and returns the request body as JSON.
        Raises ValueError if the body is not valid JSON.
        """
        if self._json_cache is not _MISSING:
            return self._json_cache
        self._json_cache = json.loads(self.body.decode("utf-8"))
        return self._json_cache

    def form(self) -> dict[str, str | list[str]]:
        """
        Parses and returns the request body as URL-encoded form data.
        """
        content_type = self.headers.get("content-type", "")
        if "application/x-www-form-urlencoded" not in content_type:
            return {}
        return self._parse_query(self.body.decode("utf-8"))

    def text(self) -> str:
        """Returns the request body decoded as UTF-8 text."""
        return self.body.decode("utf-8")

    def get_header(self, name: str, default: str = "") -> str:
        """Returns the value of a header by name (case-insensitive)."""
        return self.headers.get(name.lower(), default)

    def __repr__(self) -> str:
        return f"<Request {self.method} {self.path}>"

_MISSING = object()