__author__ = "Carlos Ruiz"

from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

class CorsMiddleware(BaseMiddleware):
    """
    Handles CORS preflight OPTIONS requests and injects CORS headers
    into all responses when cors.enabled is True.
    """

    def process(self, request: Request, next_handler: Callable) -> Response:
        cors_cfg = self.config.get("cors", {})
        if not cors_cfg.get("enabled", True):
            return next_handler(request)

        origins: list[str] = cors_cfg.get("origins", ["*"])
        methods: list[str] = cors_cfg.get(
            "methods", ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        )
        headers: list[str] = cors_cfg.get(
            "headers", ["Content-Type", "Authorization", "X-API-Key"]
        )
        allow_credentials: bool = cors_cfg.get("allow_credentials", False)
        max_age: int = cors_cfg.get("max_age", 600)

        request_origin = request.headers.get("origin", "")
        allowed_origin = _resolve_origin(request_origin, origins)

        if request.method == "OPTIONS":
            resp = Response.empty(status=204)
            _inject_cors(resp, allowed_origin, methods, headers, allow_credentials, max_age)
            return resp

        response = next_handler(request)
        _inject_cors(response, allowed_origin, methods, headers, allow_credentials, max_age)
        return response

def _resolve_origin(request_origin: str, allowed: list[str]) -> str:
    if "*" in allowed:
        return "*"
    if request_origin in allowed:
        return request_origin
    return ""

def _inject_cors(
    response: Response,
    origin: str,
    methods: list[str],
    headers: list[str],
    allow_credentials: bool,
    max_age: int,
) -> None:
    if origin:
        response.set_header("Access-Control-Allow-Origin", origin)
    response.set_header("Access-Control-Allow-Methods", ", ".join(methods))
    response.set_header("Access-Control-Allow-Headers", ", ".join(headers))
    response.set_header("Access-Control-Max-Age", str(max_age))
    if allow_credentials:
        response.set_header("Access-Control-Allow-Credentials", "true")