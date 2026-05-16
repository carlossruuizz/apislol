__author__ = "Carlos Ruiz"

import json
from typing import Any

class Response:
    """
    Represents an outgoing HTTP response.

    Attributes:
        status      HTTP status code (default 200)
        body        Response body as bytes
        headers     Dict of response headers
        content_type MIME type string
    """

    def __init__(
        self,
        body: Any = None,
        status: int = 200,
        headers: dict[str, str] | None = None,
        content_type: str = "application/json",
    ) -> None:
        self.status = status
        self.content_type = content_type
        self.headers: dict[str, str] = headers or {}
        self._raw_body = body
        self.body: bytes = self._encode(body)

    def _encode(self, body: Any) -> bytes:
        if body is None:
            return b""
        if isinstance(body, bytes):
            return body
        if isinstance(body, str):
            return body.encode("utf-8")
        return json.dumps(body, default=str).encode("utf-8")

    def set_header(self, name: str, value: str) -> "Response":
        """Sets a response header and returns self for chaining."""
        self.headers[name] = value
        return self

    def set_cookie(
        self,
        name: str,
        value: str,
        max_age: int | None = None,
        path: str = "/",
        http_only: bool = True,
        secure: bool = False,
        same_site: str = "Lax",
    ) -> "Response":
        """
        Adds a Set-Cookie header to the response.
        Returns self for chaining.
        """
        parts = [f"{name}={value}", f"Path={path}", f"SameSite={same_site}"]
        if max_age is not None:
            parts.append(f"Max-Age={max_age}")
        if http_only:
            parts.append("HttpOnly")
        if secure:
            parts.append("Secure")
        self.headers["Set-Cookie"] = "; ".join(parts)
        return self

    @classmethod
    def json(cls, data: Any, status: int = 200) -> "Response":
        """Creates a JSON response."""
        return cls(body=data, status=status, content_type="application/json")

    @classmethod
    def text(cls, data: str, status: int = 200) -> "Response":
        """Creates a plain-text response."""
        return cls(body=data, status=status, content_type="text/plain; charset=utf-8")

    @classmethod
    def html(cls, data: str, status: int = 200) -> "Response":
        """Creates an HTML response."""
        return cls(body=data, status=status, content_type="text/html; charset=utf-8")

    @classmethod
    def empty(cls, status: int = 204) -> "Response":
        """Creates an empty response (e.g., 204 No Content)."""
        return cls(body=None, status=status)

    @classmethod
    def redirect(cls, location: str, permanent: bool = False) -> "Response":
        """Creates a redirect response."""
        status = 301 if permanent else 302
        resp = cls(body=None, status=status)
        resp.set_header("Location", location)
        return resp

    @classmethod
    def error(cls, message: str, status: int = 400) -> "Response":
        """Creates a JSON error response."""
        return cls(body={"error": message}, status=status, content_type="application/json")

    def __repr__(self) -> str:
        return f"<Response {self.status} {self.content_type}>"