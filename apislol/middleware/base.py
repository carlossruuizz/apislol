__author__ = "Carlos Ruiz"

from typing import Any, Callable

from apislol.request import Request
from apislol.response import Response

NextHandler = Callable[[Request], Response]

class BaseMiddleware:
    """
    Abstract base for all middleware components.
    Subclasses must implement the `process` method.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def process(self, request: Request, next_handler: NextHandler) -> Response:
        """
        Processes the request. Must either return a Response directly
        (short-circuit) or call next_handler(request) to continue the chain.
        """
        raise NotImplementedError

class MiddlewareStack:
    """
    Composes a list of BaseMiddleware instances into a single callable chain.
    Middleware is applied in the order it appears in the list.
    """

    def __init__(self, middlewares: list[BaseMiddleware]) -> None:
        self._middlewares = middlewares

    def execute(self, request: Request, final_handler: NextHandler) -> Response:
        """
        Runs the request through the full middleware stack,
        then calls final_handler if no middleware short-circuits.
        """
        chain = final_handler
        for mw in reversed(self._middlewares):
            chain = _wrap(mw, chain)
        return chain(request)

def _wrap(middleware: BaseMiddleware, next_handler: NextHandler) -> NextHandler:
    def handler(request: Request) -> Response:
        return middleware.process(request, next_handler)
    return handler