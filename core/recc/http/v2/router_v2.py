# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPUnauthorized
from recc.log.logging import recc_http_logger as logger
from recc.driver.json import global_json_decoder
from recc.auth.bearer_auth import BearerAuth
from recc.core.context import Context
from recc.serializable.serialize import serialize_default
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http import http_header_keys as h
from recc.http import http_urls as u


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
        if not request.path.startswith(u.api_v2_public):
            await self._assign_session(request)

        try:
            return await handler(request)
        except PermissionError as e:
            logger.exception(e)
            raise HTTPUnauthorized()

    async def _assign_session(self, request: Request) -> None:
        try:
            authorization = request.headers[AUTHORIZATION]
            bearer = BearerAuth.decode_from_authorization_header(authorization)
            request[h.session] = await self.context.get_access_session(bearer.token)
        except BaseException as e:
            logger.exception(e)
            raise HTTPUnauthorized()

    def _get_routes(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            web.get(u.self, self.get_self),
            web.get(u.self_extra, self.get_self_extra),
            web.put(u.self_extra, self.put_self_extra),
        ]
        # fmt: on

    # ---------------
    # API v2 handlers
    # ---------------

    async def get_self(self, request: Request) -> Response:
        session = request[h.session]
        username = session.audience
        logger.info(f"get_self(username={username})")

        user = await self.context.get_self(session)
        user.remove_sensitive_infos()
        user.remove_unnecessary_infos()
        user_dict = serialize_default(user)
        return web.json_response(user_dict)

    async def get_self_extra(self, request: Request) -> Response:
        session = request[h.session]
        username = session.audience
        logger.info(f"get_self_extra(username={username})")

        user = await self.context.get_self(session)
        return web.json_response(user.extra)

    async def put_self_extra(self, request: Request) -> Response:
        session = request[h.session]
        username = session.audience
        extra = await request.json(loads=global_json_decoder)
        logger.info(f"put_self_extra(username={username})")

        await self.context.update_user(username, extra=extra)
        return Response()
