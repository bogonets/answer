# -*- coding: utf-8 -*-

from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPForbidden,
    HTTPServiceUnavailable,
)
from recc.logging.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.session.session_ex import SessionEx
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http.v2.router_v2_admin import RouterV2Admin
from recc.http.v2.router_v2_dev import RouterV2Dev
from recc.http.v2.router_v2_self import RouterV2Self
from recc.http.v2.router_v2_main import RouterV2Main
from recc.http.v2.router_v2_plugins import RouterV2Plugins
from recc.http.http_session import assign_session
from recc.http.http_errors import (
    HTTPReccAccessTokenError,
    HTTPReccUninitializedService,
)
from recc.http import http_urls as u
from recc.http import http_cache_keys as c


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

        self._dev = RouterV2Dev(context)
        self._app.add_subapp(u.dev, self._dev.app)

        self._self = RouterV2Self(context)
        self._app.add_subapp(u.self, self._self.app)

        self._main = RouterV2Main(context)
        self._app.add_subapp(u.main, self._main.app)

        self._plugins = RouterV2Plugins(context)
        self._app.add_subapp(u.plugins, self._plugins.app)

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    @staticmethod
    def is_admin_router(request: Request) -> bool:
        return request.path.startswith(u.api_v2_admin)

    @staticmethod
    def is_dev_router(request: Request) -> bool:
        return request.path.startswith(u.api_v2_dev)

    @staticmethod
    def is_main_router(request: Request) -> bool:
        return request.path.startswith(u.api_v2_main)

    @staticmethod
    def is_public_router(request: Request) -> bool:
        return request.path.startswith(u.api_v2_public)

    @staticmethod
    def is_self_router(request: Request) -> bool:
        return request.path.startswith(u.api_v2_self)

    @staticmethod
    def is_plugins_router(request: Request) -> bool:
        return request.path.startswith(u.api_v2_plugins)

    async def test_initialized_database(self) -> None:
        if not await self.context.is_initialized_database():
            raise HTTPReccUninitializedService

    async def assign_session(self, request: Request) -> None:
        try:
            await assign_session(self.context, request)
        except BaseException as e:
            logger.exception(e)
            raise HTTPReccAccessTokenError

    @staticmethod
    def has_admin_privileges(request: Request) -> bool:
        assert c.session in request
        session = request[c.session]
        assert isinstance(session, SessionEx)
        return session.is_admin

    async def test_admin_privileges(self, request: Request) -> None:
        if not self.has_admin_privileges(request):
            raise HTTPForbidden(reason="Administrator privileges are required")

    def test_developer_config(self) -> None:
        if not self.context.config.developer:
            raise HTTPServiceUnavailable(reason="Developer mode is not enabled")

    # -----------------------------
    # Middleware of the sub-routers
    # -----------------------------

    async def middleware_admin(self, request: Request, handler) -> Response:
        await self.test_initialized_database()
        await self.assign_session(request)
        await self.test_admin_privileges(request)
        return await handler(request)

    async def middleware_dev(self, request: Request, handler) -> Response:
        await self.test_initialized_database()
        await self.assign_session(request)
        await self.test_admin_privileges(request)
        self.test_developer_config()
        return await handler(request)

    async def middleware_main(self, request: Request, handler) -> Response:
        await self.test_initialized_database()
        await self.assign_session(request)
        return await handler(request)

    async def middleware_public(self, request: Request, handler) -> Response:
        assert self is not None, "Remove warning about 'method may be static'"
        return await handler(request)

    async def middleware_self(self, request: Request, handler) -> Response:
        await self.test_initialized_database()
        await self.assign_session(request)
        return await handler(request)

    async def middleware_plugins(self, request: Request, handler) -> Response:
        await self.test_initialized_database()
        await self.assign_session(request)
        return await handler(request)

    @web.middleware
    async def middleware(self, request: Request, handler) -> Response:
        if request.method == METH_OPTIONS:
            return await handler(request)  # (CORS) Default `options` handling.

        if self.is_admin_router(request):
            return await self.middleware_admin(request, handler)
        elif self.is_dev_router(request):
            return await self.middleware_dev(request, handler)
        elif self.is_main_router(request):
            return await self.middleware_main(request, handler)
        elif self.is_public_router(request):
            return await self.middleware_public(request, handler)
        elif self.is_self_router(request):
            return await self.middleware_self(request, handler)
        elif self.is_plugins_router(request):
            return await self.middleware_plugins(request, handler)
        else:
            raise HTTPNotFound()
