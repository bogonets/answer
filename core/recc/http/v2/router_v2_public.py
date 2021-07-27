# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPBadRequest, HTTPUnauthorized
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.driver.json import global_json_decoder
from recc.serializable.serialize import serialize_default
from recc.http.http_response import auto_response
from recc.http.http_errors import (
    HTTPReccNotInitializedError,
    HTTPReccAlreadyInitializedError,
)
from recc.http.header.basic_auth import BasicAuth
from recc.http import http_dict_keys as d
from recc.http import http_urls as u
from recc.util.version import version_text


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
            web.post(u.login, self.post_login),
        ]

    # ---------------
    # API v2 handlers
    # ---------------

    async def get_heartbeat(self, _: Request):
        assert self._context
        logger.info("get_heartbeat()")
        return Response()

    async def get_version(self, request: Request):
        assert self._context
        logger.info(f"get_version() -> {version_text}")
        return auto_response(request, version_text)

    async def get_test_init(self, _: Request):
        logger.info("get_test_init()")
        if not await self.context.exist_admin_user():
            raise HTTPReccNotInitializedError()
        return Response()

    async def post_signup_admin(self, request: Request):
        data = await request.json(loads=global_json_decoder)

        assert isinstance(data, dict)
        admin_id = data[d.admin_id]
        admin_pwd = data[d.admin_pwd]  # Perhaps the client encoded it with SHA256.
        logger.info(f"post_signup_admin({d.admin_id}={admin_id})")

        if await self.context.exist_admin_user():
            raise HTTPReccAlreadyInitializedError()

        await self.context.signup_admin(user_id=admin_id, hashed_user_pw=admin_pwd)
        return Response()

    async def post_signup(self, request: Request):
        data = await request.json(loads=global_json_decoder)

        assert isinstance(data, dict)
        user_id = data[d.user_id]
        user_pwd = data[d.user_pwd]  # Perhaps the client encoded it with SHA256.
        logger.info(f"post_signup({d.user_id}={user_id})")

        await self.context.signup(user_id=user_id, hashed_user_pw=user_pwd)
        return Response()

    async def post_login(self, request: Request):
        authorization = request.headers[AUTHORIZATION]
        auth = BasicAuth.decode_from_authorization_header(authorization)
        logger.info(f"post_login({auth})")

        try:
            username = auth.user_id
            password = auth.password
            login = await self.context.login_and_obtain_userinfo(username, password)

            access, refresh, user = login
            user.remove_sensitive_infos()
            user_dict = serialize_default(user)
            result = {d.access: access, d.refresh: refresh, d.user: user_dict}
            return web.json_response(result)
        except ValueError as e:
            logger.exception(e)
            raise HTTPBadRequest()
        except PermissionError as e:
            logger.exception(e)
            raise HTTPUnauthorized()
