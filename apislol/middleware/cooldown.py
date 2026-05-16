__author__ = "Carlos Ruiz"

import threading
import time
from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

class CooldownMiddleware(BaseMiddleware):
    """
    Tracks per-IP error occurrences and enforces a cooldown window.
    When an IP triggers a response with a status code listed in
    cooldown.trigger_on_status, it is placed in cooldown for
    cooldown.window seconds. Subsequent requests during that window
    receive a 429 response immediately.
    """

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._lock = threading.Lock()
        self._cooldowns: dict[str, float] = {}

    def process(self, request: Request, next_handler: Callable) -> Response:
        cfg = self.config.get("cooldown", {})
        if not cfg.get("enabled", False):
            return next_handler(request)

        ip = request.client_ip
        window: int = cfg.get("window", 10)
        trigger_statuses: list[int] = cfg.get("trigger_on_status", [429, 500])

        with self._lock:
            cooldown_until = self._cooldowns.get(ip, 0.0)

        if time.monotonic() < cooldown_until:
            remaining = int(cooldown_until - time.monotonic()) + 1
            resp = Response.error(
                f"Too many errors. Please wait {remaining} second(s).", status=429
            )
            resp.set_header("Retry-After", str(remaining))
            return resp

        response = next_handler(request)

        if response.status in trigger_statuses:
            with self._lock:
                self._cooldowns[ip] = time.monotonic() + window
        return response