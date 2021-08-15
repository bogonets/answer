# -*- coding: utf-8 -*-

from typing import List, Any, Dict
from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS, AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPUnauthorized,
    HTTPBadRequest,
    HTTPServiceUnavailable,
)
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_decorator import parameter_matcher
from recc.http.http_session import HttpSession
from recc.http import http_cache_keys as c
from recc.http import http_urls as u
from recc.database.struct.info import Info
from recc.database.struct.group import Group
from recc.database.struct.project import Project
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.update_password import UpdatePasswordQ
from recc.packet.update_info import UpdateInfoQ, UpdateInfoValueQ
from recc.packet.system_overview import SystemOverviewA
from recc.packet.lamda_info import LamdaInfoA
from recc.database.struct.user import User
from recc.access_control.abac.attributes import aa


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

    async def _assign_session(self, request: Request) -> None:
        try:
            authorization = request.headers[AUTHORIZATION]
            bearer = BearerAuth.decode_from_authorization_header(authorization)
            session = await self.context.get_access_session(bearer.token)
            session_user = await self.context.get_self(session, remove_sensitive=False)
            request[c.session] = session
            request[c.http_session] = HttpSession(session, session_user)
        except BaseException as e:
            logger.exception(e)
            error_message = str(e)
            if error_message:
                raise HTTPUnauthorized(reason=error_message)
            else:
                raise HTTPUnauthorized()

    @web.middleware
    async def middleware(self, request: Request, handler):
        if request.method == METH_OPTIONS:
            return await handler(request)  # Default `options` handling.

        if not request.path.startswith(u.api_v2_public):
            if not await self.context.exists_admin_user():
                raise HTTPServiceUnavailable(reason="Uninitialized server")
            await self._assign_session(request)

        return await handler(request)

    # noinspection PyTypeChecker
    def _get_routes(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            # GET: SELECT
            # PATCH: UPDATE
            # DELETE: DELETE
            # POST: INSERT, UPSERT, etc ...

            # self
            web.get(u.self, self.get_self),
            web.get(u.self_extra, self.get_self_extra),
            web.patch(u.self_extra, self.patch_self_extra),
            web.patch(u.self_password, self.patch_self_password),

            # configs
            web.get(u.configs, self.get_configs),
            web.get(u.configs_pkey, self.get_configs_pkey),
            web.patch(u.configs_pkey, self.patch_configs_pkey),

            # infos
            web.get(u.infos, self.get_infos),
            web.post(u.infos, self.post_infos),
            web.get(u.infos_pkey, self.get_infos_pkey),
            web.patch(u.infos_pkey, self.patch_infos_pkey),
            web.delete(u.infos_pkey, self.delete_infos_pkey),

            # system
            web.get(u.system_overview, self.get_system_overview),

            # system
            web.get(u.templates, self.get_templates),

            # users
            web.get(u.users, self.get_users),
            web.post(u.users, self.post_users),
            web.get(u.users_puser, self.get_users_puser),
            web.patch(u.users_puser, self.patch_users_puser),
            web.delete(u.users_puser, self.delete_users_puser),

            # groups
            web.get(u.groups, self.get_groups),
            web.post(u.groups, self.post_groups),
            web.get(u.groups_pgroup, self.get_groups_pgroup),
            web.patch(u.groups_pgroup, self.patch_groups_pgroup),
            web.delete(u.groups_pgroup, self.delete_groups_pgroup),

            # projects
            web.get(u.projects, self.get_projects),
            # web.post(u.projects, self.post_projects),
            # web.get(u.projects_pproject, self.get_projects_pproject),
            # web.patch(u.projects_pproject, self.patch_projects_pproject),
            # web.delete(u.projects_pproject, self.delete_projects_pproject),

            # # anonymous projects
            # web.get(u.projects_pproject, self.get_projects_pproject),
            # web.patch(u.projects_pproject, self.patch_projects_pproject),
            # web.delete(u.projects_pproject, self.delete_projects_pproject),
        ]
        # fmt: on

    # ----
    # Self
    # ----

    @parameter_matcher()
    async def get_self(self, hs: HttpSession) -> User:
        return hs.user

    @parameter_matcher()
    async def patch_self(self, hs: HttpSession, body: User) -> None:
        await self.context.update_user(
            hs.username,
            email=body.email,
            phone1=body.phone1,
            phone2=body.phone2,
            extra=body.extra,
        )

    @parameter_matcher()
    async def get_self_extra(self, hs: HttpSession) -> Any:
        return hs.extra

    @parameter_matcher()
    async def patch_self_extra(self, hs: HttpSession, body: Dict[str, Any]) -> None:
        await self.context.update_user_extra(hs.audience, body)

    @parameter_matcher()
    async def patch_self_password(self, hs: HttpSession, body: UpdatePasswordQ) -> None:
        try:
            if not self.context.challenge_password(hs.audience, body.before):
                raise HTTPUnauthorized(reason="The password is incorrect.")
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))
        await self.context.change_password(hs.audience, body.after)

    # -------
    # Configs
    # -------

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_configs(self) -> List[ConfigA]:
        return self.context.get_configs()

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_configs_pkey(self, key: str) -> ConfigA:
        try:
            return self.context.get_config(key)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_configs_pkey(self, key: str, body: UpdateConfigValueQ) -> None:
        try:
            self.context.update_config(key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    # -----
    # Infos
    # -----

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_infos(self) -> List[Info]:
        return await self.context.get_infos()

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_infos(self, body: UpdateInfoQ) -> None:
        try:
            await self.context.create_info(body.key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_infos_pkey(self, key: str) -> Info:
        try:
            return await self.context.get_info(key)
        except RuntimeError as e:
            raise HTTPNotFound(reason=str(e))

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_infos_pkey(self, key: str, body: UpdateInfoValueQ) -> None:
        try:
            await self.context.update_info(key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher(acl={aa.HasAdmin})
    async def delete_infos_pkey(self, key: str) -> None:
        await self.context.delete_info(key)

    # ------
    # System
    # ------

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_system_overview(self) -> SystemOverviewA:
        return await self.context.get_system_overview()

    # ---------
    # Templates
    # ---------

    @parameter_matcher()
    async def get_templates(self) -> List[LamdaInfoA]:
        return self.context.get_template_keys()

    # -----
    # Users
    # -----

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_users(self) -> List[User]:
        return await self.context.get_users()

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_users(self, body: User) -> None:
        if not body.username:
            raise HTTPBadRequest(reason="Not exists `username` field")
        if not body.password:
            raise HTTPBadRequest(reason="Not exists `password` field")

        body.strip_insensitive()
        body.empty_is_none_insensitive()

        await self.context.signup(
            username=body.username,
            hashed_password=body.password,
            nickname=body.nickname,
            email=body.email,
            phone1=body.phone1,
            phone2=body.phone2,
            is_admin=body.is_admin if body.is_admin else False,
            extra=body.extra,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_users_puser(self, hs: HttpSession, user: str) -> User:
        if hs.audience == user:
            return hs.user
        return await self.context.get_user(user)

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_users_puser(self, user: str, body: User) -> None:
        await self.context.update_user(
            user,
            nickname=body.nickname,
            email=body.email,
            phone1=body.phone1,
            phone2=body.phone2,
            is_admin=body.is_admin,
            extra=body.extra,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def delete_users_puser(self, user: str) -> None:
        await self.context.remove_user(user)

    # ------
    # Groups
    # ------

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_groups(self) -> List[Group]:
        return await self.context.get_groups()

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_groups(self, body: Group) -> None:
        if not body.slug:
            raise HTTPBadRequest(reason="Not exists `slug` field")

        await self.context.create_group(
            slug=body.slug,
            name=body.name,
            description=body.description,
            features=body.features,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_groups_pgroup(self, group: str) -> Group:
        return await self.context.get_group_by_slug(group)

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_groups_pgroup(self, group: str, body: Group) -> None:
        await self.context.update_group_by_slug(
            slug=group,
            name=body.name,
            description=body.description,
            features=body.features,
            extra=body.extra,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def delete_groups_pgroup(self, group: str) -> None:
        await self.context.delete_group_by_slug(group)

    # --------
    # Projects
    # --------

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_projects(self) -> List[Project]:
        return await self.context.get_projects()

    # @parameter_matcher(acl={aa.HasAdmin})
    # async def post_projects(self, body: Project) -> None:
    #     return await self.context.create_project(
    #         group=body.group,
    #         project=body.project,
    #         name=body.name,
    #         description=body.description,
    #         features=body.features,
    #         extra=body.extra,
    #     )

    # async def post_projects(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #
    #     data = await read_dict(request, [d.project])
    #     group_name = data.get(d.group, ANONYMOUS_GROUP_NAME)
    #     project_name = data[d.project]
    #
    #     logging_msg = f"{{ {d.group}={group_name}, {d.project}={project_name} }}"
    #     logger.info(f"post_projects(session={audience}) {logging_msg}")
    #
    #     await self.context.create_project(group_name, project_name)
    #     return self.response(request)

    # ------------------
    # Anonymous projects
    # ------------------

    # async def get_projects_pproject(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #     project_name = request.match_info[p.project]
    #     params_msg = f"session={audience},{p.project}={project_name}"
    #     logger.info(f"get_projects_pproject({params_msg})")
    #
    #     group = ANONYMOUS_GROUP_NAME
    #     project = await self.context.get_project(group, project_name)
    #     return self.response(request, serialize_default(project))
    #
    # async def patch_projects_pproject(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #     project_name = request.match_info[p.project]
    #
    #     k = project_keys
    #     data = await read_dict(request)
    #
    #     params_msg = f"session={audience},{p.project}={project_name}"
    #     logger.info(f"patch_projects_pproject({params_msg})")
    #
    #     group = ANONYMOUS_GROUP_NAME
    #     await self.context.update_project(
    #         group,
    #         project_name,
    #         name=data.get(k.name),
    #         description=data.get(k.description),
    #         features=data.get(k.features),
    #         extra=data.get(k.extra),
    #     )
    #     return Response(status=501)
    #
    # async def delete_projects_pproject(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #     project_name = request.match_info[p.project]
    #     params_msg = f"session={audience},{p.project}={project_name}"
    #     logger.info(f"delete_projects_pproject({params_msg})")
    #
    #     group = ANONYMOUS_GROUP_NAME
    #     await self.context.delete_project(group, project_name)
    #     return self.response(request)
