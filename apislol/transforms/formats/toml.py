__author__ = "Carlos Ruiz"

from typing import Any

from apislol.transforms.base import BaseTransform

class TomlTransform(BaseTransform):
    """Serializes Python dicts to TOML format without external dependencies."""

    mime_types = ["application/toml", "text/toml"]
    suffixes = [".toml"]

    def serialize(self, data: Any) -> bytes:
        if not isinstance(data, dict):
            data = {"value": data}
        return _dump_toml(data).encode("utf-8")

    @property
    def content_type(self) -> str:
        return "application/toml; charset=utf-8"

def _dump_toml(data: dict, prefix: str = "") -> str:
    lines: list[str] = []
    deferred: list[tuple[str, Any]] = []

    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            deferred.append((full_key, value))
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            deferred.append((full_key, value))
        else:
            lines.append(f"{_toml_key(key)} = {_toml_value(value)}")

    for full_key, value in deferred:
        if isinstance(value, list):
            for item in value:
                lines.append(f"\n[[{full_key}]]")
                lines.append(_dump_toml(item, ""))
        else:
            lines.append(f"\n[{full_key}]")
            lines.append(_dump_toml(value, ""))

    return "\n".join(lines)

def _toml_key(key: str) -> str:
    if key.replace("-", "").replace("_", "").isalnum():
        return key
    return f'"{key}"'

def _toml_value(value: Any) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    if isinstance(value, (list, tuple)):
        items = ", ".join(_toml_value(i) for i in value)
        return f"[{items}]"
    return f'"{str(value)}"'