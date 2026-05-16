__author__ = "Carlos Ruiz"

import ssl
import threading
import time
from typing import Any

from apislol.config import merge_config, validate_config
from apislol.logger import Logger
from apislol.middleware import (
    AllowedHostsMiddleware,
    ApiKeyMiddleware,
    BotBlockerMiddleware,
    CooldownMiddleware,
    CorsMiddleware,
    HoneypotMiddleware,
    IpFilterMiddleware,
    MiddlewareStack,
    RateLimiterMiddleware,
    UaBlocklistMiddleware,
)
from apislol.request import Request
from apislol.response import Response
from apislol.router import Router
from apislol.server import HttpServer, build_ssl_context
from apislol.transforms.registry import get_registry

class Engine:
    """
    The main application object.

    Usage:
        import apis as alol

        api = alol.engine()
        api.start(config={...})

    You can also register routes directly on the engine's router:
        @api.router.get("/ping")
        def ping(request):
            return {"pong": True}
    """

    def __init__(self) -> None:
        self.router = Router()
        self._config: dict[str, Any] = {}
        self._logger = Logger(debug=False)
        self._server: HttpServer | None = None
        self._reload_thread: threading.Thread | None = None

    def start(self, config: dict[str, Any] | None = None) -> None:
        """
        Merges config with defaults, validates it, mounts all route handlers,
        builds the middleware stack, and starts the HTTP server.
        This call blocks until the server is stopped (e.g. via KeyboardInterrupt).
        """
        merged = merge_config(config or {})
        validate_config(merged)
        self._config = merged
        self._logger = Logger(debug=merged.get("debug", False))

        self._mount_routes(merged.get("routing", {}))

        middleware_stack = self._build_middleware_stack(merged)
        ssl_context = self._build_ssl_context(merged)

        def dispatch(request: Request) -> Response:
            return middleware_stack.execute(request, self._dispatch_to_router)

        self._server = HttpServer(
            host=merged["host"],
            port=merged["port"],
            handler=dispatch,
            logger=self._logger,
            ssl_context=ssl_context,
        )

        if merged.get("auto_reload", False):
            self._start_reload_watcher(merged)

        try:
            self._server.serve_forever()
        except KeyboardInterrupt:
            self._logger.info("Shutting down.")
        finally:
            if self._server:
                self._server.shutdown()

    def stop(self) -> None:
        """Gracefully stops the running server."""
        if self._server:
            self._server.shutdown()

    def _dispatch_to_router(self, request: Request) -> Response:
        match = self.router.resolve(request.method, request.path)

        if match is None:
            if self._any_path_matches(request.path):
                return Response.error(
                    f"Method '{request.method}' not allowed.", status=405
                )
            return Response.error(f"Route '{request.path}' not found.", status=404)

        request.path_params = match.path_params

        try:
            result = match.handler(request)
        except Exception as exc:
            self._logger.error(f"Handler error: {exc}")
            return Response.error("Internal server error.", status=500)

        return self._coerce_response(result, request)

    def _coerce_response(self, result: Any, request: Request) -> Response:
        if isinstance(result, Response):
            return result

        registry = get_registry()
        accept = request.headers.get("accept", "application/json")
        transformer = registry.resolve(accept, request.path) or registry.default()

        try:
            body = transformer.serialize(result)
        except Exception:
            body = transformer.serialize({"error": "Serialization failed."})

        return Response(
            body=body,
            status=200,
            content_type=transformer.content_type,
        )

    def _mount_routes(self, routing: dict[str, str]) -> None:
        for prefix, source in routing.items():
            try:
                self.router.mount(prefix, source)
                self._logger.info(f"Mounted handler '{source}' at '{prefix}'")
            except Exception as exc:
                self._logger.error(f"Failed to mount '{source}' at '{prefix}': {exc}")

    def _build_middleware_stack(self, config: dict[str, Any]) -> MiddlewareStack:
        middlewares = [
            AllowedHostsMiddleware(config),
            IpFilterMiddleware(config),
            HoneypotMiddleware(config),
            BotBlockerMiddleware(config),
            UaBlocklistMiddleware(config),
            RateLimiterMiddleware(config),
            ApiKeyMiddleware(config),
            CooldownMiddleware(config),
            CorsMiddleware(config),
        ]
        return MiddlewareStack(middlewares)

    def _build_ssl_context(self, config: dict[str, Any]) -> ssl.SSLContext | None:
        ssl_cfg = config.get("ssl")
        if ssl_cfg is None:
            return None
        keyfile, certfile = ssl_cfg
        return build_ssl_context(keyfile, certfile)

    def _any_path_matches(self, path: str) -> bool:
        for route in self.router._routes:
            if route._regex.match(path):
                return True
        return False

    def _start_reload_watcher(self, config: dict[str, Any]) -> None:
        interval = config.get("auto_reload_interval", 2)

        def watch() -> None:
            import importlib
            import sys
            snapshots = {mod: getattr(mod, "__file__", None) for mod in sys.modules.values()}
            while True:
                time.sleep(interval)
                changed = False
                for mod in list(sys.modules.values()):
                    path = getattr(mod, "__file__", None)
                    if path and path.endswith(".py"):
                        try:
                            import os
                            mtime = os.path.getmtime(path)
                            if snapshots.get(mod) != mtime:
                                snapshots[mod] = mtime
                                changed = True
                        except OSError:
                            pass
                if changed:
                    self._logger.info("File change detected. Reload is not automatic in threaded mode — restart the server.")

        self._reload_thread = threading.Thread(target=watch, daemon=True)
        self._reload_thread.start()