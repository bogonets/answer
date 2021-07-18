# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from recc.log.logging import recc_http_logger as logger
from recc.http.http_errors import (
    HTTPReccNotInitializedError,
    HTTPReccAlreadyInitializedError,
)
from recc.auth.basic_auth import BasicAuth
from recc.core.context import Context
from recc.driver.json import global_json_decoder
from recc.http import http_dict_keys as d
from recc.http import http_urls as u
from recc.util.version import version_text


class RouterV2Public:
    """
    API version 2 for non-authentication.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application()
        self._app.add_routes(self._get_routes())

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    def _get_routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.heartbeat, self.on_heartbeat),
            web.get(u.version, self.on_version),
            web.get(u.test_init, self.on_test_init),
            web.post(u.signup_admin, self.on_signup_admin),
            web.post(u.signup, self.on_signup),
            web.post(u.login, self.on_login),
        ]

    # ---------------
    # API v2 handlers
    # ---------------

    async def on_heartbeat(self, _: Request):
        assert self._context
        logger.info("on_heartbeat()")
        return Response()

    async def on_version(self, _: Request):
        assert self._context
        logger.info(f"on_version() -> {version_text}")
        return Response(text=version_text)

    async def on_test_init(self, _: Request):
        logger.info("on_test_init()")
        if not await self.context.exist_admin_user():
            raise HTTPReccNotInitializedError()
        return Response()

    async def on_signup_admin(self, request: Request):
        data = await request.json(loads=global_json_decoder)

        assert isinstance(data, dict)
        admin_id = data[d.admin_id]
        admin_pwd = data[d.admin_pwd]  # Perhaps the client encoded it with SHA256.
        logger.info(f"on_signup_admin({d.admin_id}={admin_id})")

        if await self.context.exist_admin_user():
            raise HTTPReccAlreadyInitializedError()

        await self.context.signup_admin(user_id=admin_id, hashed_user_pw=admin_pwd)
        return Response()

    async def on_signup(self, request: Request):
        data = await request.json(loads=global_json_decoder)

        assert isinstance(data, dict)
        user_id = data[d.user_id]
        user_pwd = data[d.user_pwd]  # Perhaps the client encoded it with SHA256.
        logger.info(f"on_signup({d.user_id}={user_id})")

        await self.context.signup(user_id=user_id, hashed_user_pw=user_pwd)
        return Response()

    async def on_login(self, request: Request):
        authorization = request.headers[AUTHORIZATION]
        auth = BasicAuth.decode_from_authorization_header(authorization)
        logger.info(f"on_login({auth})")
        access, refresh = await self.context.login(auth.user_id, auth.password)
        result = {d.access: access, d.refresh: refresh}
        return web.json_response(result)
