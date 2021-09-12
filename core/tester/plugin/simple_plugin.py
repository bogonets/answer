# -*- coding: utf-8 -*-

from typing import Optional, Dict
from argparse import Namespace
from aiohttp.web_request import Request
from aiohttp.web_response import Response


class SimplePlugin:
    def __init__(self):
        self.name = "simple"

    async def on_setup(self, config: Namespace, context) -> Optional[Dict[str, str]]:
        assert config
        assert context
        return {"name": self.name}

    async def on_teardown(self) -> None:
        pass

    async def on_external(self, request: Request) -> Response:
        pass


global plugin
simple_plugin = SimplePlugin()


async def on_setup(config: Namespace, context) -> Optional[Dict[str, str]]:
    return await simple_plugin.on_setup(config, context)


async def on_teardown() -> None:
    await simple_plugin.on_teardown()


async def on_external(request: Request) -> Response:
    return await simple_plugin.on_external(request)
