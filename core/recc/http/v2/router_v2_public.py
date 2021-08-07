# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPServiceUnavailable,
)
from recc.core.context import Context
from recc.http.header.basic_auth import BasicAuth
from recc.http.http_decorator import parameter_matcher
from recc.util.version import version_text
from recc.core.struct.signup_request import SignupRequest
from recc.core.struct.signin_response import SigninResponse
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

    # noinspection PyTypeChecker
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

    @parameter_matcher
    async def get_heartbeat(self) -> None:
        pass

    @parameter_matcher
    async def get_version(self) -> str:
        return version_text

    @parameter_matcher
    async def get_test_init(self) -> None:
        if not await self.context.exists_admin_user():
            raise HTTPServiceUnavailable(reason="Uninitialized server")

    @parameter_matcher
    async def post_signup_admin(self, signup: SignupRequest) -> None:
        if await self.context.exists_admin_user():
            raise HTTPServiceUnavailable(reason="An admin account already exists")
        await self.context.signup_admin(signup.username, signup.password)

    @parameter_matcher
    async def post_signup(self, signup: SignupRequest) -> None:
        if not self.context.config.public_signup:
            raise HTTPServiceUnavailable(reason="You cannot signup without permission")
        await self.context.signup(
            username=signup.username,
            hashed_password=signup.password,
            nickname=signup.nickname,
            email=signup.email,
            phone1=signup.phone1,
            phone2=signup.phone2,
        )

    @parameter_matcher
    async def post_signin(self, auth: BasicAuth) -> SigninResponse:
        username = auth.user_id
        password = auth.password

        try:
            if not await self.context.challenge_password(username, password):
                raise HTTPUnauthorized(reason="The password is incorrect")
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))

        access, refresh = await self.context.signin(username)
        user = await self.context.get_user(username)
        return SigninResponse(access, refresh, user)
