# -*- coding: utf-8 -*-

from typing import List

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse
from aiohttp.web_routedef import AbstractRouteDef

from recc.core.context import Context
from recc.http import http_path_keys as p
from recc.http import http_urls as u
from recc.logging.logging import recc_http_logger as logger


class HttpPluginsWww:
    """
    Plugins static file router.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application(middlewares=[self.middleware])
        self._app.add_routes(self._routes())

    @property
    def app(self) -> web.Application:
        return self._app

    @web.middleware
    async def middleware(self, request: Request, handler) -> StreamResponse:
        return await handler(request)

    def _routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.pplugin_ptail, self.get_pplugin_ptail),
        ]

    async def get_pplugin_ptail(self, request: Request) -> StreamResponse:
        plugin = request.match_info[p.plugin]
        tail = request.match_info[p.tail]
        module = self._context.get_core_plugin(plugin)

        logger.debug(f"Plugin<{plugin}> GET '{tail}'")

        if module is None:
            raise HTTPNotFound(reason=f"Not found `{plugin}` plugin")

        try:
            file = module.match_www(tail)
        except KeyError as e:
            raise HTTPNotFound(reason=str(e))

        return FileResponse(file)
