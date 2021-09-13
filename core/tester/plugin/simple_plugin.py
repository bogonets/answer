# -*- coding: utf-8 -*-

from typing import Dict, Any
from aiohttp.web_request import Request
from aiohttp.web_response import Response


async def on_setup(context: Any) -> Dict[str, Any]:
    return {"name": "simple"}


async def on_teardown() -> None:
    pass


async def on_request(request: Request) -> Response:
    return Response(text="simple")
