__author__ = "Carlos Ruiz"

import re
from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

class UaBlocklistMiddleware(BaseMiddleware):
    """
    Blocks requests whose User-Agent header matches any pattern in
    config['ua_blocklist']. Each entry can be a plain string (exact
    substring match) or a regex pattern string.
    """

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._patterns: list[re.Pattern] = self._compile(config.get("ua_blocklist", []))

    def _compile(self, entries: list[str]) -> list[re.Pattern]:
        compiled = []
        for entry in entries:
            try:
                compiled.append(re.compile(entry, re.IGNORECASE))
            except re.error:
                compiled.append(re.compile(re.escape(entry), re.IGNORECASE))
        return compiled

    def process(self, request: Request, next_handler: Callable) -> Response:
        if not self._patterns:
            return next_handler(request)

        ua = request.headers.get("user-agent", "")
        for pattern in self._patterns:
            if pattern.search(ua):
                return Response.error("Forbidden: User-Agent is blocked.", status=403)
        return next_handler(request)