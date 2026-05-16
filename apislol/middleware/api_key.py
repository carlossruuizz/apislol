__author__ = "Carlos Ruiz"

import hashlib
import hmac
from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

class ApiKeyMiddleware(BaseMiddleware):
    """
    Enforces API key authentication when api_key.enabled is True.
    Keys are compared using a constant-time HMAC comparison to prevent timing attacks.
    The key is looked up first in the configured header, then in query parameters.
    """

    def process(self, request: Request, next_handler: Callable) -> Response:
        api_cfg = self.config.get("api_key", {})
        if not api_cfg.get("enabled", False):
            return next_handler(request)

        valid_keys: list[str] = api_cfg.get("keys", [])
        if not valid_keys:
            return next_handler(request)

        header_name: str = api_cfg.get("header", "X-API-Key").lower()
        query_param: str = api_cfg.get("query_param", "api_key")

        provided = request.headers.get(header_name) or str(
            request.query.get(query_param, "")
        )

        if not provided:
            return Response.error("API key required.", status=401)

        for key in valid_keys:
            if _safe_compare(provided, key):
                return next_handler(request)

        return Response.error("Invalid API key.", status=403)

def _safe_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(
        hashlib.sha256(a.encode()).digest(),
        hashlib.sha256(b.encode()).digest(),
    )