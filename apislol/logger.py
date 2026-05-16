__author__ = "Carlos Ruiz"

import sys
import datetime

class Logger:
    """
    Simple logger that writes to stderr.
    All output is suppressed when debug is False.
    """

    def __init__(self, debug: bool = False) -> None:
        self.debug_mode = debug

    def info(self, message: str) -> None:
        if self.debug_mode:
            self._write("INFO", message)

    def warning(self, message: str) -> None:
        if self.debug_mode:
            self._write("WARN", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def debug(self, message: str) -> None:
        if self.debug_mode:
            self._write("DEBUG", message)

    def _write(self, level: str, message: str) -> None:
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"[{timestamp}] [{level}] {message}", file=sys.stderr, flush=True)