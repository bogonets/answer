# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPServiceUnavailable,
)
from recc.core.context import Context
from recc.http.header.basic_auth import BasicAuth
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_parameter import parameter_matcher
from recc.util.version import version_text
from recc.packet.user import UserA, SigninA, SignupQ, RefreshTokenA
from recc.packet.preference import PreferenceA
from recc.http import http_urls as u


class RouterV2Public:
    """
    API version 2 for non-authentication.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application()
        self._app.add_routes(self._routes())

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    # noinspection PyTypeChecker
    def _routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.heartbeat, self.get_heartbeat),
            web.get(u.version, self.get_version),
            web.get(u.state_already, self.get_state_already),
            web.post(u.signup_admin, self.post_signup_admin),
            web.post(u.signup, self.post_signup),
            web.post(u.signin, self.post_signin),
            web.post(u.token_refresh, self.post_token_refresh),
        ]

    # --------
    # Handlers
    # --------

    @parameter_matcher
    async def get_heartbeat(self) -> None:
        pass

    @parameter_matcher
    async def get_version(self) -> str:
        return version_text

    @parameter_matcher
    async def get_state_already(self) -> bool:
        return await self.context.is_initialized_database()

    @parameter_matcher
    async def post_signup(self, body: SignupQ) -> None:
        if not self.context.config.public_signup:
            raise HTTPServiceUnavailable(reason="You cannot signup without permission")
        await self.context.signup_guest(
            username=body.username,
            hashed_password=body.password,
            nickname=body.nickname,
            email=body.email,
            phone1=body.phone1,
            phone2=body.phone2,
        )

    @parameter_matcher
    async def post_signup_admin(self, signup: SignupQ) -> None:
        if await self.context.is_initialized_database():
            raise HTTPServiceUnavailable(reason="An admin account already exists")
        await self.context.signup_admin(signup.username, signup.password)

    @parameter_matcher
    async def post_signin(self, auth: BasicAuth) -> SigninA:
        username = auth.user_id
        password = auth.password

        try:
            if not await self.context.challenge_password(username, password):
                raise HTTPUnauthorized(reason="The password is incorrect")
        except RuntimeError as e:
            # maybe `not found user`
            raise HTTPBadRequest(reason=str(e))
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))

        access, refresh = await self.context.signin(username)
        user_uid = await self.context.get_user_uid(username)
        db_user = await self.context.get_user(user_uid)
        oem = await self.context.opt_info_oem_value()
        assert db_user.username is not None
        user = UserA(
            username=db_user.username,
            nickname=db_user.nickname,
            email=db_user.email,
            phone1=db_user.phone1,
            phone2=db_user.phone2,
            is_admin=db_user.is_admin if db_user.is_admin else False,
            extra=db_user.extra,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login,
        )
        preference = PreferenceA(oem=oem)
        return SigninA(access, refresh, user, preference)

    # -----
    # Token
    # -----

    @parameter_matcher
    async def post_token_refresh(self, bearer: BearerAuth) -> RefreshTokenA:
        refresh_token = bearer.token
        token = await self.context.renew_access_token(refresh_token)
        return RefreshTokenA(access=token)
