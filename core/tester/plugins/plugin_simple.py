# -*- coding: utf-8 -*-

from aiohttp.web_response import Response


def on_create(context, **kwargs) -> None:
    pass


def on_destroy() -> None:
    pass


async def on_open() -> None:
    pass


async def on_close() -> None:
    pass


async def on_request(request) -> Response:
    return Response(text="simple")
