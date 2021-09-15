# -*- coding: utf-8 -*-

def on_create(context, **kwargs) -> None:
    pass


def on_destroy() -> None:
    pass


async def on_open() -> None:
    pass


async def on_close() -> None:
    pass


async def on_request() -> str:
    return "simple"
