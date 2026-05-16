__author__ = "Carlos Ruiz"

from typing import Any

class BaseTransform:
    """
    Abstract base class for response body transformers.

    Subclasses must declare:
        mime_types  — list of MIME type strings this transformer handles
        suffixes    — list of URL suffixes (e.g. '.json') that trigger this transformer
    And implement:
        serialize(data) — converts data to bytes
        content_type    — property returning the primary MIME type string
    """

    mime_types: list[str] = []
    suffixes: list[str] = []

    def serialize(self, data: Any) -> bytes:
        """Converts data to the target format and returns bytes."""
        raise NotImplementedError

    @property
    def content_type(self) -> str:
        """Returns the primary Content-Type string for this format."""
        return self.mime_types[0] if self.mime_types else "application/octet-stream"