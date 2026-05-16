__author__ = "Carlos Ruiz"

import ipaddress
from typing import Callable

from apislol.middleware.base import BaseMiddleware
from apislol.request import Request
from apislol.response import Response

class IpFilterMiddleware(BaseMiddleware):
    """
    Blocks requests from IPs on the blacklist and, when a whitelist is
    configured, only allows requests from IPs on the whitelist.

    Both lists support individual IPs and CIDR notation (e.g. '10.0.0.0/8').
    Whitelist takes precedence: if both lists are non-empty and the IP is
    on the whitelist, it is allowed regardless of the blacklist.
    """

    def process(self, request: Request, next_handler: Callable) -> Response:
        blacklist: list[str] = self.config.get("ip_blacklist", [])
        whitelist: list[str] = self.config.get("ip_whitelist", [])
        ip = request.client_ip

        if whitelist:
            if not _ip_in_list(ip, whitelist):
                return Response.error("Forbidden: your IP is not whitelisted.", status=403)
            return next_handler(request)

        if blacklist and _ip_in_list(ip, blacklist):
            return Response.error("Forbidden: your IP has been blocked.", status=403)

        return next_handler(request)

def _ip_in_list(ip: str, entries: list[str]) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False

    for entry in entries:
        try:
            if "/" in entry:
                if addr in ipaddress.ip_network(entry, strict=False):
                    return True
            else:
                if addr == ipaddress.ip_address(entry):
                    return True
        except ValueError:
            continue
    return False