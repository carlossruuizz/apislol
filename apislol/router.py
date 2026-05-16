__author__ = "Carlos Ruiz"

import importlib.util
import inspect
import os
import re
import sys
from typing import Any, Callable

from apislol.request import Request
from apislol.response import Response

RouteHandler = Callable[[Request], Response | dict]

class RouteMatch:
    """Holds the result of a successful route match."""

    def __init__(self, handler: RouteHandler, path_params: dict[str, str]) -> None:
        self.handler = handler
        self.path_params = path_params

class Route:
    """
    Represents a single registered route.
    Compiles the path pattern into a regex for efficient matching.
    """

    PARAM_PATTERN = re.compile(r"\{(\w+)\}")

    def __init__(self, method: str, path: str, handler: RouteHandler) -> None:
        self.method = method.upper()
        self.path = path
        self.handler = handler
        self.param_names: list[str] = self.PARAM_PATTERN.findall(path)
        self._regex = self._compile(path)

    def _compile(self, path: str) -> re.Pattern:
        escaped = re.escape(path)
        pattern = self.PARAM_PATTERN.sub(
            lambda m: f"(?P<{m.group(1)}>[^/]+)",
            escaped.replace(r"\{", "{").replace(r"\}", "}"),
        )
        return re.compile(f"^{pattern}$")

    def match(self, method: str, path: str) -> dict[str, str] | None:
        """
        Returns a dict of path parameters if this route matches, otherwise None.
        """
        if self.method not in (method.upper(), "*"):
            return None
        m = self._regex.match(path)
        if m is None:
            return None
        return m.groupdict()

class Router:
    """
    Central routing table.
    Supports registering handlers for specific HTTP methods and paths,
    as well as loading handler modules from file paths or import strings.
    """

    def __init__(self) -> None:
        self._routes: list[Route] = []
        self._prefix_modules: dict[str, Any] = {}

    def add_route(self, method: str, path: str, handler: RouteHandler) -> None:
        """Registers a handler for a specific method and path."""
        self._routes.append(Route(method, path, handler))

    def get(self, path: str) -> Callable:
        """Decorator for registering a GET handler."""
        def decorator(fn: RouteHandler) -> RouteHandler:
            self.add_route("GET", path, fn)
            return fn
        return decorator

    def post(self, path: str) -> Callable:
        """Decorator for registering a POST handler."""
        def decorator(fn: RouteHandler) -> RouteHandler:
            self.add_route("POST", path, fn)
            return fn
        return decorator

    def put(self, path: str) -> Callable:
        """Decorator for registering a PUT handler."""
        def decorator(fn: RouteHandler) -> RouteHandler:
            self.add_route("PUT", path, fn)
            return fn
        return decorator

    def delete(self, path: str) -> Callable:
        """Decorator for registering a DELETE handler."""
        def decorator(fn: RouteHandler) -> RouteHandler:
            self.add_route("DELETE", path, fn)
            return fn
        return decorator

    def patch(self, path: str) -> Callable:
        """Decorator for registering a PATCH handler."""
        def decorator(fn: RouteHandler) -> RouteHandler:
            self.add_route("PATCH", path, fn)
            return fn
        return decorator

    def mount(self, prefix: str, source: str) -> None:
        """
        Loads a handler module from a file path or dotted import string
        and registers all routes it exposes under the given prefix.

        The module must expose a `router` attribute (a Router instance)
        or a `routes` list of (method, path, handler) tuples,
        or individual handler functions decorated with HTTP method names.
        """
        module = _load_module(source, prefix)
        self._prefix_modules[prefix] = module
        self._register_module_routes(prefix, module)

    def resolve(self, method: str, path: str) -> RouteMatch | None:
        """
        Finds the first matching route for the given method and path.
        Returns a RouteMatch or None if no route matches.
        """
        for route in self._routes:
            params = route.match(method, path)
            if params is not None:
                return RouteMatch(route.handler, params)
        return None

    def _register_module_routes(self, prefix: str, module: Any) -> None:
        if hasattr(module, "router") and isinstance(module.router, Router):
            for route in module.router._routes:
                full_path = (prefix.rstrip("/") + "/" + route.path.lstrip("/")).rstrip("/") or "/"
                self.add_route(route.method, full_path, route.handler)
            return

        if hasattr(module, "routes") and isinstance(module.routes, list):
            for entry in module.routes:
                method, path, handler = entry
                full_path = (prefix.rstrip("/") + "/" + path.lstrip("/")).rstrip("/") or "/"
                self.add_route(method, full_path, handler)
            return

        for name in dir(module):
            obj = getattr(module, name)
            if callable(obj) and hasattr(obj, "_apislol_method"):
                method = obj._apislol_method
                path = getattr(obj, "_apislol_path", f"/{name}")
                full_path = (prefix.rstrip("/") + "/" + path.lstrip("/")).rstrip("/") or "/"
                self.add_route(method, full_path, obj)

def _load_module(source: str, prefix: str) -> Any:
    """
    Loads a Python module from a file path (e.g. './handlers/users.py')
    or a dotted import string (e.g. 'myapp.handlers.users').
    """
    if source.endswith(".py") or os.sep in source or "/" in source:
        return _load_from_file(source, prefix)
    return _load_from_import(source)


def _load_from_file(path: str, prefix: str) -> Any:
    abs_path = os.path.abspath(path)
    module_name = f"_apislol_handler_{prefix.strip('/').replace('/', '_') or 'root'}"
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load handler module from: {abs_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def _load_from_import(dotted: str) -> Any:
    return importlib.import_module(dotted)

def route(method: str, path: str) -> Callable:
    """
    Decorator for marking a standalone function as a route handler.
    Used when a handler module exposes individual functions rather than a router.

    Example:
        @route("GET", "/{id}")
        def get_user(request):
            ...
    """
    def decorator(fn: Callable) -> Callable:
        fn._apislol_method = method.upper()
        fn._apislol_path = path
        return fn
    return decorator