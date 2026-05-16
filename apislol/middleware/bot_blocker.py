__author__ = "Carlos Ruiz"

import re
from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

KNOWN_BOT_PATTERNS: list[str] = [
    r"Googlebot",
    r"Bingbot",
    r"Slurp",
    r"DuckDuckBot",
    r"Baiduspider",
    r"YandexBot",
    r"Sogou",
    r"Exabot",
    r"facebot",
    r"ia_archiver",
    r"Scrapy",
    r"python-requests",
    r"Go-http-client",
    r"curl/",
    r"wget/",
    r"libwww-perl",
    r"Java/",
    r"okhttp",
    r"axios/",
    r"node-fetch",
    r"undici",
    r"GPTBot",
    r"ChatGPT-User",
    r"CCBot",
    r"anthropic-ai",
    r"Claude-Web",
    r"cohere-ai",
    r"PerplexityBot",
    r"YouBot",
    r"PhantomJS",
    r"HeadlessChrome",
    r"Selenium",
    r"puppeteer",
    r"playwright",
    r"SemrushBot",
    r"AhrefsBot",
    r"MJ12bot",
    r"DotBot",
    r"rogerbot",
    r"linkdexbot",
    r"archive\.org_bot",
    r"HTTrack",
    r"WebCopier",
    r"SiteSnagger",
    r"WebReaper",
    r"Offline Explorer",
    r"Teleport Pro",
]

_COMPILED_BOTS = re.compile("|".join(KNOWN_BOT_PATTERNS), re.IGNORECASE)

class BotBlockerMiddleware(BaseMiddleware):
    """
    Blocks requests whose User-Agent matches known bot, scraper, or AI crawler patterns.
    Also blocks requests with empty or missing User-Agent headers.
    Only active when block_bots is True in config.
    """

    def process(self, request: Request, next_handler: Callable) -> Response:
        if not self.config.get("block_bots", True):
            return next_handler(request)

        ua = request.headers.get("user-agent", "")

        if not ua.strip():
            return Response.error("Forbidden: missing User-Agent.", status=403)

        if _COMPILED_BOTS.search(ua):
            return Response.error("Forbidden: automated clients are not allowed.", status=403)

        return next_handler(request)