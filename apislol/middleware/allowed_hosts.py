__author__ = "Carlos Ruiz"

from typing import Any, Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

class AllowedHostsMiddleware(BaseMiddleware):
    """
    Validates the Host header against the configured allowed_hosts list.
    Returns 400 Bad Request if the host is not permitted.
    Skips validation when allowed_hosts is empty or contains '*'.
    """

    def process(self, request: Request, next_handler: Callable) -> Response:
        allowed = self.config.get("allowed_hosts", [])
        if not allowed or "*" in allowed:
            return next_handler(request)

        host = request.headers.get("host", "").split(":")[0].strip()
        if host not in allowed:
            return Response.error(f"Host '{host}' is not allowed.", status=400)
        return next_handler(request)