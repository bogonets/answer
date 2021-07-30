# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS, AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPNotFound
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.serializable.serialize import serialize_default
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_response import auto_response
from recc.http.http_request import read_dict

from recc.http import http_data_keys as d
from recc.http import http_header_keys as h
from recc.http import http_path_keys as p
from recc.http import http_urls as u

from recc.variables.database import ANONYMOUS_GROUP_NAME


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
            web.patch(u.self_extra, self.patch_self_extra),

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

            # projects
            web.get(u.projects, self.get_projects),
            web.post(u.projects, self.post_projects),
            # anonymous projects
            web.get(u.projects_pproject, self.get_projects_pproject),
            web.patch(u.projects_pproject, self.patch_projects_pproject),
            web.delete(u.projects_pproject, self.delete_projects_pproject),
        ]
        # fmt: on

    # ----
    # Self
    # ----

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

    async def patch_self_extra(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        extra = await read_dict(request)
        logger.info(f"patch_self_extra(session={audience})")

        await self.context.update_user(audience, extra=extra)
        return Response()

    # -------
    # Configs
    # -------

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
        data = await read_dict(request, [d.key, d.val])
        key = data[d.key]
        val = data[d.val]
        logging_msg = f"{{{d.key}={key},{d.val}={val}}}"
        logger.info(f"post_configs(session={audience}) {logging_msg}")

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

    # -----
    # Users
    # -----

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
        data = await read_dict(request, [d.username, d.password])
        username = data[d.username]
        password = data[d.password]
        logger.info(f"post_users(session={audience})")

        await self.context.signup(
            username=username,
            hashed_password=password,
            email=data.get(d.email),
            phone1=data.get(d.phone1),
            phone2=data.get(d.phone2),
            is_admin=data.get(d.is_admin),
            extra=data.get(d.extra),
        )
        return Response()

    async def get_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        logger.info(f"get_users_puser(session={audience},{p.user}={username})")

        user = await self.context.get_user(session, username)
        user_dict = serialize_default(user)
        return auto_response(request, user_dict)

    async def patch_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        data = await read_dict(request)
        logger.info(f"patch_users_puser(session={audience},{p.user}={username})")

        await self.context.update_user(
            username,
            email=data.get(d.email),
            phone1=data.get(d.phone1),
            phone2=data.get(d.phone2),
            is_admin=data.get(d.is_admin),
            extra=data.get(d.extra),
        )
        return Response()

    async def delete_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        logger.info(f"delete_users_puser(session={audience},{p.user}={username})")
        await self.context.remove_user(username)
        return Response()

    # --------
    # Projects
    # --------

    async def get_projects(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        group_name = ANONYMOUS_GROUP_NAME
        logger.info(f"get_projects(session={audience})")

        projects = await self.context.get_projects(session, group_name)
        for project in projects:
            project.remove_sensitive_fields()
        projects_dict = serialize_default(projects)
        return auto_response(request, projects_dict)

    async def post_projects(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience

        data = await read_dict(request, [d.project])
        group_name = data.get(d.group, ANONYMOUS_GROUP_NAME)
        project_name = data[d.project]

        logging_msg = f"{{{d.group}={group_name},{d.project}={project_name}}}"
        logger.info(f"post_projects(session={audience}) {logging_msg}")

        await self.context.create_project(session, group_name, project_name)
        return Response()

    # ------------------
    # Anonymous projects
    # ------------------

    async def get_projects_pproject(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        project_name = request.match_info[p.project]
        params_msg = f"session={audience},{p.project}={project_name}"
        logger.info(f"get_projects_pproject({params_msg})")

        group = ANONYMOUS_GROUP_NAME
        project = await self.context.get_project(session, group, project_name)
        return auto_response(request, serialize_default(project))

    async def patch_projects_pproject(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        project_name = request.match_info[p.project]
        data = await read_dict(request)
        params_msg = f"session={audience},{p.project}={project_name}"
        logger.info(f"patch_projects_pproject({params_msg})")

        group = ANONYMOUS_GROUP_NAME
        await self.context.update_project(
            session,
            group,
            project_name,
            name=data.get(d.name),
            description=data.get(d.description),
            features=data.get(d.features),
            extra=data.get(d.extra),
        )
        return Response(status=501)

    async def delete_projects_pproject(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        project_name = request.match_info[p.project]
        params_msg = f"session={audience},{p.project}={project_name}"
        logger.info(f"delete_projects_pproject({params_msg})")

        group = ANONYMOUS_GROUP_NAME
        await self.context.delete_project(session, group, project_name)
        return Response()
