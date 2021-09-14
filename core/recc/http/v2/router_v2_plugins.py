# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from recc.core.context import Context
from recc.http.http_decorator import parameter_matcher
from recc.http import http_urls as u
from recc.http import http_path_keys as p


class RouterV2Plugins:
    """
    API version 2 for plugins.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application()
        self._app.add_routes(self._routes())

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    # noinspection PyTypeChecker
    def _routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.empty, self.get_root),
            web.get(u.root, self.get_root),
            web.get(u.pplugin_ptail, self.get_plugin_tail),
            web.patch(u.pplugin_ptail, self.patch_plugin_tail),
            web.post(u.pplugin_ptail, self.post_plugin_tail),
            web.delete(u.pplugin_ptail, self.delete_plugin_tail),
        ]

    # --------
    # Handlers
    # --------

    @parameter_matcher()
    async def get_root(self) -> List[str]:
        return self.context.get_plugin_keys()

    async def any_plugin_tail(self, request: Request) -> Response:
        plugin = request.match_info[p.plugin]
        return await self.context.plugins.request(plugin, request)

    async def get_plugin_tail(self, request: Request) -> Response:
        return await self.any_plugin_tail(request)

    async def patch_plugin_tail(self, request: Request) -> Response:
        return await self.any_plugin_tail(request)

    async def post_plugin_tail(self, request: Request) -> Response:
        return await self.any_plugin_tail(request)

    async def delete_plugin_tail(self, request: Request) -> Response:
        return await self.any_plugin_tail(request)
