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
from recc.core.struct.signup import Signup
from recc.core.struct.signin import Signin
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
            web.get(u.state_already, self.get_state_already),
            web.post(u.signup_admin, self.post_signup_admin),
            web.post(u.signup, self.post_signup),
            web.post(u.signin, self.post_signin),
        ]

    # ---------------
    # API v2 handlers
    # ---------------

    async def _already(self) -> bool:
        return await self.context.exists_admin_user()

    @parameter_matcher()
    async def get_heartbeat(self) -> None:
        pass

    @parameter_matcher()
    async def get_version(self) -> str:
        return version_text

    @parameter_matcher()
    async def get_state_already(self) -> bool:
        return await self._already()

    @parameter_matcher()
    async def post_signup_admin(self, signup: Signup) -> None:
        if await self._already():
            raise HTTPServiceUnavailable(reason="An admin account already exists")
        await self.context.signup_admin(signup.username, signup.password)

    @parameter_matcher()
    async def post_signup(self, signup: Signup) -> None:
        if not self.context.config.public_signup:
            raise HTTPServiceUnavailable(reason="You cannot signup without permission")
        await self.context.signup_guest(signup)

    @parameter_matcher()
    async def post_signin(self, auth: BasicAuth) -> Signin:
        username = auth.user_id
        password = auth.password

        try:
            if not await self.context.challenge_password(username, password):
                raise HTTPUnauthorized(reason="The password is incorrect")
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))

        access, refresh = await self.context.signin(username)
        user = await self.context.get_user(username)
        return Signin(access, refresh, user)
