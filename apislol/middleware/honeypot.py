__author__ = "Carlos Ruiz"

import threading
import time
from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

HONEYPOT_BAN_DURATION = 3600

class HoneypotMiddleware(BaseMiddleware):
    """
    Any request to a path listed in config['honeypots'] results in the
    requesting IP being banned for HONEYPOT_BAN_DURATION seconds.
    Subsequent requests from that IP receive a 403 Forbidden response.
    """

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._lock = threading.Lock()
        self._banned: dict[str, float] = {}

    def process(self, request: Request, next_handler: Callable) -> Response:
        honeypots: list[str] = self.config.get("honeypots", [])
        ip = request.client_ip

        with self._lock:
            ban_until = self._banned.get(ip, 0.0)

        if time.monotonic() < ban_until:
            return Response.error("Forbidden.", status=403)

        if request.path in honeypots:
            with self._lock:
                self._banned[ip] = time.monotonic() + HONEYPOT_BAN_DURATION
            return Response.error("Forbidden.", status=403)

        return next_handler(request)