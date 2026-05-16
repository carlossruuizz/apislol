"""
Static handler — serves the frontend for arduino_recommend.
"""

import os

from apislol.router import Router
from apislol.request import Request
from apislol.response import Response

router = Router()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@router.get("/")
def index(request: Request) -> Response:
    path = os.path.join(BASE_DIR, "static", "index.html")
    with open(path, "rb") as f:
        return Response(body=f.read(), status=200, content_type="text/html; charset=utf-8")


@router.get("/styles/{filename}")
def styles(request: Request) -> Response:
    path = os.path.join(BASE_DIR, "static", "styles", request.path_params["filename"])
    return _serve(path, "text/css")


@router.get("/js/{filename}")
def scripts(request: Request) -> Response:
    path = os.path.join(BASE_DIR, "static", "js", request.path_params["filename"])
    return _serve(path, "application/javascript")


def _serve(path: str, ct: str) -> Response:
    if not os.path.isfile(path):
        return Response.error("Not found.", status=404)
    with open(path, "rb") as f:
        return Response(body=f.read(), status=200, content_type=ct)
