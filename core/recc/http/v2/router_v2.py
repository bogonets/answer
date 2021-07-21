# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPBadRequest, HTTPUnauthorized
from recc.log.logging import recc_http_logger as logger
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
            web.get(u.user, self.on_user),
        ]
        # fmt: on

    # ---------------
    # API v2 handlers
    # ---------------

    async def on_user(self, request: Request) -> Response:
        session = request[h.session]
        username = session.audience
        logger.info(f"on_user(username={username})")

        try:
            user = await self.context.get_user(session, username)
        except ValueError as e:
            logger.exception(e)
            raise HTTPBadRequest()
        except PermissionError as e:
            logger.exception(e)
            raise HTTPUnauthorized()

        user.remove_sensitive_infos()
        user.remove_unnecessary_infos()
        user_dict = serialize_default(user)
        return web.json_response(user_dict)
