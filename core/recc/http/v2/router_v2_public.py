# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPServiceUnavailable,
)
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.serializable.serialize import serialize_default
from recc.http.http_response import auto_response
from recc.http.http_request import read_dict
from recc.http.header.basic_auth import BasicAuth
from recc.util.version import version_text
from recc.core.struct.request.signup import keys as signup_keys
from recc.core.struct.response.login import Login
from recc.http import http_data_keys as d
from recc.http import http_urls as u


class RouterV2Public:
    """
    API version 2 for non-authentication.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application(middlewares=[self.middleware])
        self._app.add_routes(self._get_routes())

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
        return [
            web.get(u.heartbeat, self.get_heartbeat),
            web.get(u.version, self.get_version),
            web.get(u.test_init, self.get_test_init),
            web.post(u.signup_admin, self.post_signup_admin),
            web.post(u.signup, self.post_signup),
            web.post(u.signin, self.post_signin),
        ]

    # ---------------
    # API v2 handlers
    # ---------------

    async def get_heartbeat(self, _: Request) -> Response:
        assert self._context
        logger.info("get_heartbeat()")
        return Response()

    async def get_version(self, request: Request) -> Response:
        assert self._context
        logger.info(f"get_version() -> {version_text}")
        return auto_response(request, version_text)

    async def get_test_init(self, _: Request) -> Response:
        logger.info("get_test_init()")
        if not await self.context.exists_admin_user():
            raise HTTPServiceUnavailable(reason="Uninitialized server")
        return Response()

    async def post_signup_admin(self, request: Request) -> Response:
        if await self.context.exists_admin_user():
            raise HTTPServiceUnavailable(reason="An admin account already exists")

        k = signup_keys
        data = await read_dict(request, [k.username, k.password])
        username = data[k.username]
        password = data[k.password]  # Perhaps the client encoded it with SHA256.

        logger.info(f"post_signup_admin() {{ {k.username}={username} }}")

        await self.context.signup_admin(username, password)
        return Response()

    async def post_signup(self, request: Request) -> Response:
        if not self.context.config.public_signup:
            raise HTTPServiceUnavailable(reason="You cannot signup without permission.")

        k = signup_keys
        data = await read_dict(request, [k.username, k.password])
        username = data[k.username]
        password = data[k.password]  # Perhaps the client encoded it with SHA256.
        logger.info(f"post_signup({d.username}={username})")

        await self.context.signup(
            username=username,
            hashed_password=password,
            nickname=data.get(k.nickname),
            email=data.get(k.email),
            phone1=data.get(k.phone1),
            phone2=data.get(k.phone2),
        )
        return Response()

    async def post_signin(self, request: Request) -> Response:
        try:
            authorization = request.headers[AUTHORIZATION]
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

        try:
            auth = BasicAuth.decode_from_authorization_header(authorization)
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))

        logger.info(f"post_signin({auth})")
        username = auth.user_id
        password = auth.password

        try:
            if not await self.context.challenge_password(username, password):
                raise HTTPUnauthorized(reason="The password is incorrect.")
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))

        access, refresh = await self.context.signin(username)
        user = await self.context.get_user(username)

        result = serialize_default(Login(access, refresh, user))
        return auto_response(request, result)
