"""
Static handler — serves the frontend HTML for cats_image.
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
    filename = request.path_params["filename"]
    path = os.path.join(BASE_DIR, "static", "styles", filename)
    return _serve_file(path, "text/css")


@router.get("/js/{filename}")
def scripts(request: Request) -> Response:
    filename = request.path_params["filename"]
    path = os.path.join(BASE_DIR, "static", "js", filename)
    return _serve_file(path, "application/javascript")


@router.get("/assets/{filename}")
def assets(request: Request) -> Response:
    filename = request.path_params["filename"]
    path = os.path.join(BASE_DIR, "static", "assets", filename)
    mime = "image/png" if filename.endswith(".png") else "image/svg+xml"
    return _serve_file(path, mime)


@router.get("/favicon.ico")
def favicon(request: Request) -> Response:
    return Response.empty(status=204)


def _serve_file(path: str, content_type: str) -> Response:
    if not os.path.isfile(path):
        return Response.error("Not found.", status=404)
    with open(path, "rb") as f:
        return Response(body=f.read(), status=200, content_type=content_type)
