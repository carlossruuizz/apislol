__author__ = "Carlos Ruiz"

import html
from typing import Any

from apislol.transforms.base import BaseTransform

class HtmlTransform(BaseTransform):
    """Serializes Python objects to a minimal, readable HTML page."""

    mime_types = ["text/html"]
    suffixes = [".html", ".htm"]

    def serialize(self, data: Any) -> bytes:
        body_content = _render(data)
        page = (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "<head>\n"
            '  <meta charset="UTF-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            "  <title>Response</title>\n"
            "  <style>\n"
            "    body { font-family: sans-serif; padding: 2rem; }\n"
            "    table { border-collapse: collapse; width: 100%; }\n"
            "    th, td { border: 1px solid #ccc; padding: 0.5rem 1rem; text-align: left; }\n"
            "    th { background: #f0f0f0; }\n"
            "  </style>\n"
            "</head>\n"
            f"<body>\n{body_content}\n</body>\n</html>"
        )
        return page.encode("utf-8")

    @property
    def content_type(self) -> str:
        return "text/html; charset=utf-8"

def _render(data: Any) -> str:
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return _render_table(data)
    if isinstance(data, dict):
        return _render_table([data])
    if isinstance(data, list):
        items = "".join(f"<li>{html.escape(str(i))}</li>" for i in data)
        return f"<ul>{items}</ul>"
    return f"<p>{html.escape(str(data))}</p>"

def _render_table(rows: list[dict]) -> str:
    all_keys: list[str] = []
    for row in rows:
        for k in row:
            if k not in all_keys:
                all_keys.append(k)

    header = "".join(f"<th>{html.escape(str(k))}</th>" for k in all_keys)
    body_rows = []
    for row in rows:
        cells = "".join(
            f"<td>{html.escape(str(row.get(k, '')))}</td>" for k in all_keys
        )
        body_rows.append(f"<tr>{cells}</tr>")

    return (
        "<table>\n"
        f"  <thead><tr>{header}</tr></thead>\n"
        f"  <tbody>{''.join(body_rows)}</tbody>\n"
        "</table>"
    )