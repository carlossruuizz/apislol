"""
apislol:
Build HTTP APIs in pure Python with zero dependencies and minimal boilerplate.

A lightweight framework with a built-in security middleware stack, flexible routing,
and multi-format response transforms.

GitHub: https://github.com/carlossruuizz
"""

__author__ = "Carlos Ruiz"
__version__ = "1.0.0"
__license__ = "MIT"

from apislol.engine import Engine
from apislol.request import Request
from apislol.response import Response

def engine() -> Engine:
    """
    Factory function that creates and returns a new Engine instance.
    This is the primary entry point for building an apislol application.
    """
    return Engine()

__all__ = [
    "engine",
    "Engine",
    "Request",
    "Response",
]