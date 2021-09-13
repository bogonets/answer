# -*- coding: utf-8 -*-

from typing import Dict, Any
from recc.plugin.plugin import Plugin
from aiohttp.web_request import Request
from aiohttp.web_response import Response


class PluginManager(Dict[str, Plugin]):
    def exists_create(self, name: str) -> bool:
        return self.__getitem__(name).exists_create

    def exists_destroy(self, name: str) -> bool:
        return self.__getitem__(name).exists_destroy

    def exists_open(self, name: str) -> bool:
        return self.__getitem__(name).exists_open

    def exists_close(self, name: str) -> bool:
        return self.__getitem__(name).exists_close

    def exists_request(self, name: str) -> bool:
        return self.__getitem__(name).exists_request

    def call_create(self, name: str, context: Any, **kwargs) -> None:
        self.__getitem__(name).call_create(context, **kwargs)

    def call_destroy(self, name: str) -> None:
        self.__getitem__(name).call_destroy()

    async def call_open(self, name: str) -> None:
        await self.__getitem__(name).call_open()

    async def call_close(self, name: str) -> None:
        await self.__getitem__(name).call_close()

    async def call_request(self, name: str, request: Request) -> Response:
        return await self.__getitem__(name).call_request(request)
