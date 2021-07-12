# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.hdrs import AUTHORIZATION
from recc.log.logging import recc_http_logger as logger
from recc.auth.bearer_auth import BearerAuth
from recc.core.context import Context
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http import http_urls as u
from recc.session.session import Session
from recc.util.version import version_text


class RouterV2:
    """
    API version 2 - HTTP Router class.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application(middlewares=[self.middleware])
        self._app.add_routes(self._get_routes())

        self._public = RouterV2Public(context)
        self._app.add_subapp(u.public, self._public.app)

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    @web.middleware
    async def middleware(self, request: Request, handler):
        return await handler(request)

    def _get_routes(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            web.get("/version", self.on_version),
        ]
        # fmt: on

    async def _get_access_session(self, request: Request) -> Session:
        authorization = request.headers[AUTHORIZATION]
        auth = BearerAuth.decode_from_authorization_header(authorization)
        return await self._context.get_access_session(auth.token)

    # ---------------
    # API v2 handlers
    # ---------------

    async def on_version(self, _: Request):
        assert self._context
        logger.info(f"on_version() -> {version_text}")
        return Response(text=version_text)
