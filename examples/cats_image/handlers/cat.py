"""
Cat handler — fetches a random cat image from cataas.com (no API key required).
"""

import json
import urllib.request
import urllib.error

from apislol.router import Router
from apislol.request import Request
from apislol.response import Response

router = Router()

CATAAS_URL = "https://cataas.com/cat?json=true"


@router.get("/")
def random_cat(request: Request) -> Response:
    """Returns a random cat image URL and metadata as JSON."""
    try:
        req = urllib.request.Request(
            CATAAS_URL,
            headers={"User-Agent": "apislol-cats-example/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())

        cat_id = data.get("id", "")
        url = data.get("url") or f"https://cataas.com/cat/{cat_id}"
        tags = data.get("tags", [])

        return Response.json({
            "id": cat_id,
            "url": url,
            "tags": tags,
        })
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError) as exc:
        return Response.error(f"Could not fetch cat image: {exc}", status=502)
