# -*- coding: utf-8 -*-

from typing import Dict, Any
from asyncio import gather
from recc.plugin.plugin import Plugin
from aiohttp.web_request import Request
from aiohttp.web_response import Response


class PluginManager(Dict[str, Plugin]):
    def create(self, context: Any, *files: str, **kwargs) -> None:
        for file in files:
            plugin = Plugin(file)
            if plugin.exists_create:
                plugin.call_create(context, **kwargs)
            self.__setitem__(plugin.name, plugin)

    def destroy(self) -> None:
        for key, plugin in self.items():
            if plugin.exists_destroy:
                plugin.call_destroy()

    async def open(self) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_open:
                coroutines.append(plugin.call_open())
        await gather(*coroutines)

    async def close(self) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_close:
                coroutines.append(plugin.call_close())
        await gather(*coroutines)

    async def request(self, name: str, request: Request) -> Response:
        plugin = self.__getitem__(name)
        if not plugin.exists_request:
            raise NotImplementedError
        return await plugin.call_request(request)
