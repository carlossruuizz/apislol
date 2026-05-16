__author__ = "Carlos Ruiz"

import xml.etree.ElementTree as ET
from typing import Any

from apislol.transforms.base import BaseTransform

class XmlTransform(BaseTransform):
    """Serializes Python objects to XML using the standard library."""

    mime_types = ["application/xml", "text/xml"]
    suffixes = [".xml"]

    def serialize(self, data: Any) -> bytes:
        root = ET.Element("response")
        _build_element(root, data)
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        return ET.tostring(root, encoding="unicode", xml_declaration=False).encode("utf-8")

    @property
    def content_type(self) -> str:
        return "application/xml; charset=utf-8"

def _build_element(parent: ET.Element, data: Any) -> None:
    if data is None:
        parent.text = ""
    elif isinstance(data, bool):
        parent.text = "true" if data else "false"
    elif isinstance(data, (int, float, str)):
        parent.text = str(data)
    elif isinstance(data, dict):
        for key, value in data.items():
            safe_key = _safe_tag(str(key))
            child = ET.SubElement(parent, safe_key)
            _build_element(child, value)
    elif isinstance(data, (list, tuple)):
        for item in data:
            child = ET.SubElement(parent, "item")
            _build_element(child, item)
    else:
        parent.text = str(data)

def _safe_tag(name: str) -> str:
    if not name or name[0].isdigit():
        name = f"_{name}"
    return "".join(c if c.isalnum() or c in ("_", "-", ".") else "_" for c in name)