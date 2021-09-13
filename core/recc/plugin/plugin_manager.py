# -*- coding: utf-8 -*-

from typing import Dict, Any
from recc.plugin.plugin import Plugin
from aiohttp.web_request import Request
from aiohttp.web_response import Response


class PluginManager(Dict[str, Plugin]):
    def exists_setup(self, name: str) -> bool:
        return self.__getitem__(name).exists_setup()

    def exists_teardown(self, name: str) -> bool:
        return self.__getitem__(name).exists_teardown()

    def exists_request(self, name: str) -> bool:
        return self.__getitem__(name).exists_request()

    async def call_setup(self, name: str, context: Any, **kwargs) -> None:
        await self.__getitem__(name).call_setup(context, **kwargs)

    async def call_teardown(self, name: str) -> None:
        await self.__getitem__(name).call_teardown()

    async def call_request(self, name: str, request: Request) -> Response:
        return await self.__getitem__(name).call_request(request)
