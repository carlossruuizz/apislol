__author__ = "Carlos Ruiz"

import collections
import threading
import time
from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

class RateLimiterMiddleware(BaseMiddleware):
    """
    Implements a sliding-window rate limiter.

    The limit and window are read from config:
        rate_limit       — maximum number of requests allowed per window (default 60)
        rate_limit_window — window size in seconds (default 60)

    The client is identified by API key (if present) or by IP address.
    Clients that exceed the limit receive a 429 Too Many Requests response
    with a Retry-After header.
    """

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._lock = threading.Lock()
        self._windows: dict[str, collections.deque] = {}

    def process(self, request: Request, next_handler: Callable) -> Response:
        limit: int = self.config.get("rate_limit", 60)
        if limit == 0:
            return next_handler(request)

        window: int = self.config.get("rate_limit_window", 60)
        client_id = self._identify(request)
        now = time.monotonic()

        with self._lock:
            if client_id not in self._windows:
                self._windows[client_id] = collections.deque()

            timestamps = self._windows[client_id]
            cutoff = now - window
            while timestamps and timestamps[0] < cutoff:
                timestamps.popleft()

            if len(timestamps) >= limit:
                retry_after = int(window - (now - timestamps[0])) + 1
                resp = Response.error("Rate limit exceeded.", status=429)
                resp.set_header("Retry-After", str(retry_after))
                resp.set_header("X-RateLimit-Limit", str(limit))
                resp.set_header("X-RateLimit-Remaining", "0")
                return resp

            timestamps.append(now)
            remaining = limit - len(timestamps)

        response = next_handler(request)
        response.set_header("X-RateLimit-Limit", str(limit))
        response.set_header("X-RateLimit-Remaining", str(remaining))
        return response

    def _identify(self, request: Request) -> str:
        api_cfg = self.config.get("api_key", {})
        if api_cfg.get("enabled", False):
            header_name = api_cfg.get("header", "X-API-Key").lower()
            key = request.headers.get(header_name, "")
            if key:
                return f"key:{key}"
        return f"ip:{request.client_ip}"