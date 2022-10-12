# -*- coding: utf-8 -*-

import os
from typing import List

from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse
from aiohttp.web_routedef import AbstractRouteDef

from recc.core.context import Context
from recc.filesystem.permission import is_readable_dir, is_writable_dir
from recc.http import http_path_keys as p
from recc.http import http_urls as u
from recc.logging.logging import recc_http_logger as logger


class HttpWWW:
    """
    Static file router.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application(middlewares=[self.middleware])
        self._app.add_routes(self._routes())

        self.logging_validation()

    def logging_validation(self) -> None:
        path = self._context.config.http_root
        if not os.path.isdir(path):
            logger.error(f"Not found http root directory: {path}")
        if not is_readable_dir(path):
            logger.error(f"Not readable http root directory: {path}")
        if is_writable_dir(path):
            logger.warning(
                f"Writable http root directory (There may be a security issue): {path}"
            )

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    @web.middleware
    async def middleware(self, request: Request, handler) -> StreamResponse:
        return await handler(request)

    def _routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.empty, self.get_root),
            web.get(u.ppath, self.get_path),
        ]

    async def get_root(self, request: Request) -> StreamResponse:
        raise web.HTTPFound(u.app_root)

    async def get_path(self, request: Request) -> StreamResponse:
        http_root = self._context.config.http_root
        path = request.match_info[p.path]
        logger.debug(f"WWW GET '{path}'")

        file = os.path.join(http_root, path)
        if os.path.isfile(file):
            return FileResponse(file)

        # SPA(Single Page Application) reads only one page (file).
        return FileResponse(os.path.join(http_root, "index.html"))
