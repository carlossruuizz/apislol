__author__ = "Carlos Ruiz"

import json
from typing import Any

from apislol.transforms.base import BaseTransform

class JsonTransform(BaseTransform):
    """Serializes Python objects to JSON."""

    mime_types = ["application/json", "text/json"]
    suffixes = [".json"]

    def serialize(self, data: Any) -> bytes:
        return json.dumps(data, default=str, ensure_ascii=False).encode("utf-8")

    @property
    def content_type(self) -> str:
        return "application/json; charset=utf-8"