# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS, AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPNotFound, HTTPBadRequest
from recc.log.logging import recc_http_logger as logger
from recc.driver.json import global_json_decoder
from recc.core.context import Context
from recc.serializable.serialize import serialize_default
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_response import auto_response

from recc.http import http_data_keys as d
from recc.http import http_header_keys as h
from recc.http import http_path_keys as p
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
            if request.method == METH_OPTIONS:
                return await handler(request)
            else:
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
            # self
            web.get(u.self, self.get_self),
            web.get(u.self_extra, self.get_self_extra),
            web.post(u.self_extra, self.post_self_extra),

            # configs
            web.get(u.configs, self.get_configs),
            web.post(u.configs, self.post_configs),
            web.get(u.configs_pkey, self.get_configs_pkey),

            # users
            web.get(u.users, self.get_users),
            web.post(u.users, self.post_users),
            web.get(u.users_puser, self.get_users_puser),
            web.patch(u.users_puser, self.patch_users_puser),
            web.delete(u.users_puser, self.delete_users_puser),
        ]
        # fmt: on

    # ---------------
    # API v2 handlers
    # ---------------

    async def get_self(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"get_self(session={audience})")

        session_user = await self.context.get_self(session)
        session_user.remove_sensitive_infos()
        user_dict = serialize_default(session_user)
        return web.json_response(user_dict)

    async def get_self_extra(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"get_self_extra(session={audience})")

        session_user = await self.context.get_self(session)
        return web.json_response(session_user.extra)

    async def post_self_extra(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        extra = await request.json(loads=global_json_decoder)
        logger.info(f"post_self_extra(session={audience})")

        await self.context.update_user(audience, extra=extra)
        return Response()

    async def get_configs(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"get_configs(session={audience})")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        configs = await self.context.get_configs()
        result = {config.key: config.val for config in configs}
        return web.json_response(result)

    async def post_configs(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience

        data = await request.json(loads=global_json_decoder)
        if not isinstance(data, dict):
            raise HTTPBadRequest(reason="Only dictionary-type requests are accepted")
        key = data.get(d.key)
        if key is None:
            raise HTTPBadRequest(reason=f"Not exists `{d.key}`")
        val = data.get(d.val)
        if val is None:
            raise HTTPBadRequest(reason=f"Not exists `{d.val}`")

        logger.info(f"post_configs(session={audience}) config(key={key},val={val})")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        await self.context.set_config(key, val)
        return Response()

    async def get_configs_pkey(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        key = request.match_info[p.key]
        logger.info(f"get_configs_pkey(session={audience},key={key})")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        try:
            config = await self.context.get_config(key)
            return auto_response(request, config.val)
        except BaseException as e:  # noqa
            logger.exception(e)
            raise HTTPNotFound(reason=f"Not found config: {key}")

    async def get_users(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"get_users(session={audience})")

        users = await self.context.get_users(session)
        users_dict = serialize_default(users)
        return auto_response(request, users_dict)

    async def post_users(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"post_users(session={audience})")
        return Response(status=501)

    async def get_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        logger.info(f"get_users_puser(session={audience},username={username})")

        user = await self.context.get_user(session, username)
        user_dict = serialize_default(user)
        return auto_response(request, user_dict)

    async def patch_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        logger.info(f"patch_users_puser(session={audience},key={username})")
        return Response(status=501)

    async def delete_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        logger.info(f"delete_users_puser(session={audience},key={username})")
        await self.context.remove_user(username)
        return Response()
