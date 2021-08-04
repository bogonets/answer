# -*- coding: utf-8 -*-

from typing import List, Any
from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS, AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPBadRequest
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

# from recc.database.struct.group import keys as group_keys
# from recc.database.struct.group_member import keys as group_member_keys

from recc.database.struct.info import keys as info_keys

# from recc.database.struct.layout import keys as layout_keys
# from recc.database.struct.permission import keys as permission_keys
# from recc.database.struct.port import keys as port_keys

from recc.database.struct.project import keys as project_keys

# from recc.database.struct.project_member import keys as project_member_keys
# from recc.database.struct.task import keys as task_keys

from recc.database.struct.user import keys as user_keys

# from recc.database.struct.widget import keys as widget_keys

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
            # GET: SELECT
            # PATCh: UPDATE
            # DELETE: DELETE
            # POST: INSERT, UPSERT, etc ...

            # self
            web.get(u.self, self.get_self),
            web.get(u.self_extra, self.get_self_extra),
            web.patch(u.self_extra, self.patch_self_extra),

            # configs
            web.get(u.infos, self.get_infos),
            web.post(u.infos, self.post_infos),
            web.get(u.infos_pkey, self.get_infos_pkey),
            web.delete(u.infos_pkey, self.delete_infos_pkey),

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

    def response(self, request: Request, data: Any = None) -> Response:
        if data is None:
            if self.context.config.verbose >= 2:
                logger.debug(f"{request.method} {request.path}")
            return Response()
        else:
            result = auto_response(request, data)
            if self.context.config.verbose >= 2:
                logger.debug(f"{request.method} {request.path} -> {data}")
            return result

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
        return self.response(request, user_dict)

    async def get_self_extra(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"get_self_extra(session={audience})")

        session_user = await self.context.get_self(session)
        return self.response(request, session_user.extra)

    async def patch_self_extra(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        extra = await read_dict(request)
        logger.info(f"patch_self_extra(session={audience})")

        await self.context.update_user(audience, extra=extra)
        return self.response(request)

    # -----
    # Infos
    # -----

    async def get_infos(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"get_infos(session={audience})")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        configs = await self.context.get_infos()
        result = {config.key: config.value for config in configs}
        return self.response(request, result)

    async def post_infos(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience

        dk = info_keys  # Data Key
        data = await read_dict(request, [dk.key, dk.value])
        key = data[dk.key]
        value = data[dk.value]

        logging_msg = f"{{ {dk.key}={key}, {dk.value}={value} }}"
        logger.info(f"post_infos(session={audience}) {logging_msg}")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        await self.context.set_info(key, value)
        return self.response(request)

    async def get_infos_pkey(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        key = request.match_info[p.key]
        logger.info(f"get_infos_pkey(session={audience},key={key})")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        config = await self.context.get_info(key)
        return self.response(request, config.value)

    async def delete_infos_pkey(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        key = request.match_info[p.key]
        logger.info(f"delete_infos_pkey(session={audience},key={key})")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        await self.context.delete_info(key)
        return self.response(request)

    # -----
    # Users
    # -----

    async def get_users(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        logger.info(f"get_users(session={audience})")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        users = await self.context.get_users()
        users_dict = serialize_default(users)
        return self.response(request, users_dict)

    async def post_users(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience

        dk = user_keys
        data = await read_dict(request, [dk.username, dk.password])
        username = data[dk.username]
        hashed_password = data[dk.password]

        if not username:
            raise HTTPBadRequest(reason=f"`{dk.username}` is empty.")
        if not hashed_password:
            raise HTTPBadRequest(reason=f"`{dk.password}` is empty.")

        logger.info(f"post_users(session={audience}) -> username={username}")

        await self.context.signup(
            username=username,
            hashed_password=hashed_password,
            email=data.get(dk.email),
            phone1=data.get(dk.phone1),
            phone2=data.get(dk.phone2),
            is_admin=data.get(dk.is_admin),
            extra=data.get(dk.extra),
        )
        return self.response(request)

    async def get_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        logger.info(f"get_users_puser(session={audience},{p.user}={username})")

        session_user = await self.context.get_self(session)
        if session.audience == username:
            user = session_user
        else:
            if not session_user.is_admin:
                raise HTTPUnauthorized(reason="Administrator privileges are required")
            user = await self.context.get_user(username)

        user_dict = serialize_default(user)
        return self.response(request, user_dict)

    async def patch_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]

        dk = user_keys
        data = await read_dict(request)

        logger.info(f"patch_users_puser(session={audience},{p.user}={username})")

        await self.context.update_user(
            username,
            email=data.get(dk.email),
            phone1=data.get(dk.phone1),
            phone2=data.get(dk.phone2),
            is_admin=data.get(dk.is_admin),
            extra=data.get(dk.extra),
        )
        return self.response(request)

    async def delete_users_puser(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        username = request.match_info[p.user]
        logger.info(f"delete_users_puser(session={audience},{p.user}={username})")
        await self.context.remove_user(username)
        return self.response(request)

    # --------
    # Projects
    # --------

    async def get_projects(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        group_name = ANONYMOUS_GROUP_NAME
        logger.info(f"get_projects(session={audience})")

        projects = await self.context.get_projects(group_name)
        for project in projects:
            project.remove_sensitive_fields()
        projects_dict = serialize_default(projects)
        return self.response(request, projects_dict)

    async def post_projects(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience

        data = await read_dict(request, [d.project])
        group_name = data.get(d.group, ANONYMOUS_GROUP_NAME)
        project_name = data[d.project]

        logging_msg = f"{{ {d.group}={group_name}, {d.project}={project_name} }}"
        logger.info(f"post_projects(session={audience}) {logging_msg}")

        await self.context.create_project(group_name, project_name)
        return self.response(request)

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
        project = await self.context.get_project(group, project_name)
        return self.response(request, serialize_default(project))

    async def patch_projects_pproject(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        project_name = request.match_info[p.project]

        dk = project_keys
        data = await read_dict(request)

        params_msg = f"session={audience},{p.project}={project_name}"
        logger.info(f"patch_projects_pproject({params_msg})")

        group = ANONYMOUS_GROUP_NAME
        await self.context.update_project(
            group,
            project_name,
            name=data.get(dk.name),
            description=data.get(dk.description),
            features=data.get(dk.features),
            extra=data.get(dk.extra),
        )
        return Response(status=501)

    async def delete_projects_pproject(self, request: Request) -> Response:
        session = request[h.session]
        audience = session.audience
        project_name = request.match_info[p.project]
        params_msg = f"session={audience},{p.project}={project_name}"
        logger.info(f"delete_projects_pproject({params_msg})")

        group = ANONYMOUS_GROUP_NAME
        await self.context.delete_project(group, project_name)
        return self.response(request)
