__author__ = "Carlos Ruiz"

from typing import Any

from apislol.transforms.base import BaseTransform

class YamlTransform(BaseTransform):
    """
    Serializes Python objects to YAML format.
    Implemented without external dependencies using a minimal recursive emitter.
    """

    mime_types = ["application/x-yaml", "text/yaml", "text/x-yaml"]
    suffixes = [".yaml", ".yml"]

    def serialize(self, data: Any) -> bytes:
        return _dump(data).encode("utf-8")

    @property
    def content_type(self) -> str:
        return "text/yaml; charset=utf-8"

def _dump(obj: Any, indent: int = 0) -> str:
    pad = "  " * indent
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        return str(obj)
    if isinstance(obj, str):
        return _quote_string(obj)
    if isinstance(obj, (list, tuple)):
        if not obj:
            return "[]"
        lines = []
        for item in obj:
            rendered = _dump(item, indent + 1)
            if isinstance(item, dict):
                first_line, *rest = rendered.splitlines()
                lines.append(f"{pad}- {first_line}")
                for line in rest:
                    lines.append(f"{pad}  {line}")
            else:
                lines.append(f"{pad}- {rendered}")
        return "\n".join(lines)
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        lines = []
        for key, value in obj.items():
            rendered = _dump(value, indent + 1)
            if isinstance(value, (dict, list)) and value:
                lines.append(f"{pad}{key}:")
                for line in rendered.splitlines():
                    lines.append(f"  {line}")
            else:
                lines.append(f"{pad}{key}: {rendered}")
        return "\n".join(lines)
    return _quote_string(str(obj))

def _quote_string(s: str) -> str:
    needs_quoting = any(c in s for c in (':', '#', '[', ']', '{', '}', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`', '"', "'", '\n', '\r'))
    if needs_quoting or not s:
        escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
        return f'"{escaped}"'
    return s