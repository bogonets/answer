# -*- coding: utf-8 -*-

from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS
from aiohttp.web_request import Request
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPServiceUnavailable
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http.v2.router_v2_admin import RouterV2Admin
from recc.http.v2.router_v2_self import RouterV2Self
from recc.http.v2.router_v2_main import RouterV2Main
from recc.http.http_session import assign_session
from recc.http import http_urls as u


class RouterV2:
    """
    API version 2 - HTTP Router class.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application(middlewares=[self.middleware])

        self._public = RouterV2Public(context)
        self._app.add_subapp(u.public, self._public.app)

        self._admin = RouterV2Admin(context)
        self._app.add_subapp(u.admin, self._admin.app)

        self._self = RouterV2Self(context)
        self._app.add_subapp(u.self, self._self.app)

        self._main = RouterV2Main(context)
        self._app.add_subapp(u.main, self._main.app)

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    @staticmethod
    def is_public_router(request: Request) -> bool:
        return request.path.startswith(u.api_v2_public)

    @web.middleware
    async def middleware(self, request: Request, handler):
        if request.method == METH_OPTIONS:
            return await handler(request)  # Default `options` handling.

        if self.is_public_router(request):
            return await handler(request)

        if not await self.context.is_initialized_database():
            raise HTTPServiceUnavailable(reason="Uninitialized service")

        try:
            await assign_session(self.context, request)
        except BaseException as e:
            logger.exception(e)
            raise HTTPUnauthorized(reason=str(e))

        return await handler(request)
