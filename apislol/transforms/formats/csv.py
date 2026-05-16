__author__ = "Carlos Ruiz"

import csv
import io
from typing import Any

from apislol.transforms.base import BaseTransform

class CsvTransform(BaseTransform):
    """
    Serializes Python data to CSV format.
    Expects a list of dicts (rows) or a single dict (one row).
    Other types are wrapped in a single-column table.
    """

    mime_types = ["text/csv"]
    suffixes = [".csv"]

    def serialize(self, data: Any) -> bytes:
        buf = io.StringIO()
        writer_kwargs = {"lineterminator": "\r\n"}

        if isinstance(data, list) and data and isinstance(data[0], dict):
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(buf, fieldnames=fieldnames, **writer_kwargs)
            writer.writeheader()
            writer.writerows(data)
        elif isinstance(data, dict):
            fieldnames = list(data.keys())
            writer = csv.DictWriter(buf, fieldnames=fieldnames, **writer_kwargs)
            writer.writeheader()
            writer.writerow(data)
        else:
            writer = csv.writer(buf, **writer_kwargs)
            writer.writerow(["value"])
            if isinstance(data, (list, tuple)):
                for item in data:
                    writer.writerow([item])
            else:
                writer.writerow([data])

        return buf.getvalue().encode("utf-8")

    @property
    def content_type(self) -> str:
        return "text/csv; charset=utf-8"