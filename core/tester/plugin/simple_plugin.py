# -*- coding: utf-8 -*-

from typing import Optional, Dict, Any
from aiohttp.web_request import Request
from aiohttp.web_response import Response


def on_setup(config, context) -> Optional[Dict[str, Any]]:
    return {"name": "simple"}


def on_teardown() -> None:
    pass


def on_external(request: Request) -> Response:
    pass
