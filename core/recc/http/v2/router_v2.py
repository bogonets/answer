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
from recc.access_control.abac.attributes import aa
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_decorator import parameter_matcher
from recc.http.http_session import HttpSession
from recc.http import http_cache_keys as c
from recc.http import http_urls as u
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.info import InfoA, CreateInfoQ, UpdateInfoQ
from recc.packet.permission import PermissionA, CreatePermissionQ, UpdatePermissionQ
from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
from recc.packet.system import SystemOverviewA
from recc.packet.template import TemplateA
from recc.packet.user import UserA, UpdateUserQ, SignupQ, UpdatePasswordQ


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

            audience_uid = await self.context.get_user_uid(session.audience)
            session_user = await self.context.get_user(
                audience_uid, remove_sensitive=False
            )

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
            # self/profile
            web.get(u.self, self.get_self),
            web.get(u.self_extra, self.get_self_extra),
            web.patch(u.self_extra, self.patch_self_extra),
            web.patch(u.self_password, self.patch_self_password),

            # self/groups
            web.get(u.self_groups, self.get_self_groups),
            web.post(u.self_groups, self.post_self_groups),
            web.get(u.self_groups_pgroup, self.get_self_groups_pgroup),
            web.patch(u.self_groups_pgroup, self.patch_self_groups_pgroup),
            web.delete(u.self_groups_pgroup, self.delete_self_groups_pgroup),

            # self/projects
            web.get(u.self_projects, self.get_self_projects),
            web.post(u.self_projects, self.post_self_projects),
            web.get(u.self_projects_pgroup_pproject, self.get_self_projects_pgroup_pproject),  # noqa
            web.patch(u.self_projects_pgroup_pproject, self.patch_self_projects_pgroup_pproject),  # noqa
            web.delete(u.self_projects_pgroup_pproject, self.delete_self_projects_pgroup_pproject),  # noqa

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
            web.post(u.projects, self.post_projects),
            web.get(u.projects_pgroup_pproject, self.get_projects_pgroup_pproject),
            web.patch(u.projects_pgroup_pproject, self.patch_projects_pgroup_pproject),
            web.delete(u.projects_pgroup_pproject, self.delete_projects_pgroup_pproject),  # noqa

            # permissions
            web.get(u.permissions, self.get_permissions),
            web.post(u.permissions, self.post_permissions),
            web.get(u.permissions_pperm, self.get_permissions_pperm),
            web.patch(u.permissions_pperm, self.patch_permissions_pperm),
            web.delete(u.permissions_pperm, self.delete_permissions_pperm),
        ]
        # fmt: on

    # ----
    # Self
    # ----

    @parameter_matcher()
    async def get_self(self, hs: HttpSession) -> UserA:
        return UserA(
            username=hs.username,
            nickname=hs.nickname,
            email=hs.email,
            phone1=hs.phone1,
            phone2=hs.phone2,
            is_admin=hs.is_admin,
            extra=hs.extra,
            created_at=hs.created_at,
            updated_at=hs.updated_at,
            last_login=hs.last_login,
        )

    @parameter_matcher()
    async def patch_self(self, hs: HttpSession, body: UpdateUserQ) -> None:
        await self.context.update_user(
            uid=hs.uid,
            email=body.email,
            phone1=body.phone1,
            phone2=body.phone2,
            is_admin=None,
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

    # -----------
    # self/groups
    # -----------

    @parameter_matcher()
    async def get_self_groups(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def post_self_groups(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def get_self_groups_pgroup(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def patch_self_groups_pgroup(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def delete_self_groups_pgroup(self, hs: HttpSession) -> None:
        raise NotImplementedError

    # -------------
    # self/projects
    # -------------

    @parameter_matcher()
    async def get_self_projects(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def post_self_projects(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def get_self_projects_pgroup_pproject(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def patch_self_projects_pgroup_pproject(self, hs: HttpSession) -> None:
        raise NotImplementedError

    @parameter_matcher()
    async def delete_self_projects_pgroup_pproject(self, hs: HttpSession) -> None:
        raise NotImplementedError

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
    async def get_infos(self) -> List[InfoA]:
        result = list()
        for info in await self.context.get_infos():
            assert info.key
            item = InfoA(
                key=info.key,
                value=info.value,
                created_at=info.created_at,
                updated_at=info.updated_at,
            )
            result.append(item)
        return result

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_infos(self, body: CreateInfoQ) -> None:
        try:
            await self.context.create_info(body.key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_infos_pkey(self, key: str) -> InfoA:
        try:
            db_info = await self.context.get_info(key)
        except RuntimeError as e:
            raise HTTPNotFound(reason=str(e))
        assert db_info.key
        return InfoA(
            key=db_info.key,
            value=db_info.value,
            created_at=db_info.created_at,
            updated_at=db_info.updated_at,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_infos_pkey(self, key: str, body: UpdateInfoQ) -> None:
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

    # ------
    # Lamdas
    # ------

    @parameter_matcher()
    async def get_templates(self) -> List[TemplateA]:
        return self.context.get_template_keys()

    # -----
    # Users
    # -----

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_users(self) -> List[UserA]:
        result = list()
        for user in await self.context.get_users():
            assert user.username
            item = UserA(
                username=user.username,
                nickname=user.nickname,
                email=user.email,
                phone1=user.phone1,
                phone2=user.phone2,
                is_admin=user.is_admin,
                extra=user.extra,
                created_at=user.created_at,
                updated_at=user.updated_at,
                last_login=user.last_login,
            )
            result.append(item)
        return result

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_users(self, body: SignupQ) -> None:
        if not body.username:
            raise HTTPBadRequest(reason="Not exists `username` field")
        if not body.password:
            raise HTTPBadRequest(reason="Not exists `password` field")

        body.strip()
        body.empty_is_none()

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
    async def get_users_puser(self, hs: HttpSession, user: str) -> UserA:
        if hs.audience == user:
            return UserA(
                username=hs.username,
                nickname=hs.nickname,
                email=hs.email,
                phone1=hs.phone1,
                phone2=hs.phone2,
                is_admin=hs.is_admin,
                extra=hs.extra,
                created_at=hs.created_at,
                updated_at=hs.updated_at,
                last_login=hs.last_login,
            )
        else:
            user_uid = await self.context.get_user_uid(user)
            db_user = await self.context.get_user(user_uid)
            assert db_user.username
            return UserA(
                username=db_user.username,
                nickname=db_user.nickname,
                email=db_user.email,
                phone1=db_user.phone1,
                phone2=db_user.phone2,
                is_admin=db_user.is_admin,
                extra=db_user.extra,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at,
                last_login=db_user.last_login,
            )

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_users_puser(self, user: str, body: UpdateUserQ) -> None:
        body.strip()
        body.empty_is_none()
        user_uid = await self.context.get_user_uid(user)
        await self.context.update_user(
            uid=user_uid,
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
    async def get_groups(self) -> List[GroupA]:
        result = list()
        for group in await self.context.get_groups():
            assert group.slug is not None
            item = GroupA(
                slug=group.slug,
                name=group.name,
                description=group.description,
                features=group.features,
                extra=group.extra,
                created_at=group.created_at,
                updated_at=group.updated_at,
            )
            result.append(item)
        return result

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_groups(self, body: CreateGroupQ) -> None:
        if not body.slug:
            raise HTTPBadRequest(reason="Not exists `slug` field")
        await self.context.create_group(
            slug=body.slug,
            name=body.name,
            description=body.description,
            features=body.features,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_groups_pgroup(self, group: str) -> GroupA:
        group_uid = await self.context.get_group_uid(group)
        db_group = await self.context.get_group(group_uid)
        assert db_group.slug is not None
        return GroupA(
            slug=db_group.slug,
            name=db_group.name,
            description=db_group.description,
            features=db_group.features,
            extra=db_group.extra,
            created_at=db_group.created_at,
            updated_at=db_group.updated_at,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_groups_pgroup(self, group: str, body: UpdateGroupQ) -> None:
        group_uid = await self.context.get_group_uid(group)
        await self.context.update_group(
            uid=group_uid,
            name=body.name,
            description=body.description,
            features=body.features,
            extra=body.extra,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def delete_groups_pgroup(self, group: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        await self.context.delete_group(group_uid)

    # --------
    # Projects
    # --------

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_projects(self) -> List[ProjectA]:
        result = list()
        for project in await self.context.get_projects(remove_sensitive=False):
            assert project.uid is not None
            assert project.group_uid is not None
            assert project.slug is not None
            item = ProjectA(
                await self.context.get_group_slug(project.group_uid),
                project.slug,
                project.name,
                project.description,
                project.features,
                project.extra,
                project.created_at,
                project.updated_at,
            )
            result.append(item)
        return result

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_projects(self, body: CreateProjectQ) -> None:
        group_uid = await self.context.get_group_uid(body.group_slug)
        await self.context.create_project(
            group_uid=group_uid,
            slug=body.project_slug,
            name=body.name,
            description=body.description,
            features=body.features,
            extra=body.extra,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_projects_pgroup_pproject(self, group: str, project: str) -> ProjectA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        db_project = await self.context.get_project(project_uid)
        return ProjectA(
            group_slug=group,
            project_slug=project,
            name=db_project.name,
            description=db_project.description,
            features=db_project.features,
            extra=db_project.extra,
            created_at=db_project.created_at,
            updated_at=db_project.updated_at,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_projects_pgroup_pproject(
        self, group: str, project: str, body: UpdateProjectQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        await self.context.update_project(
            uid=project_uid,
            name=body.name,
            description=body.description,
            features=body.features,
            extra=body.extra,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def delete_projects_pgroup_pproject(self, group: str, project: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        await self.context.delete_project(project_uid)

    # -----------
    # Permissions
    # -----------

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_permissions(self) -> List[PermissionA]:
        result = list()
        for permission in await self.context.get_permissions():
            assert permission.name is not None
            item = PermissionA(
                name=permission.name,
                description=permission.description,
                features=permission.features,
                extra=permission.extra,
                r_layout=permission.r_layout,
                w_layout=permission.w_layout,
                r_storage=permission.r_storage,
                w_storage=permission.w_storage,
                r_manager=permission.r_manager,
                w_manager=permission.w_manager,
                r_graph=permission.r_graph,
                w_graph=permission.w_graph,
                r_member=permission.r_member,
                w_member=permission.w_member,
                r_setting=permission.r_setting,
                w_setting=permission.w_setting,
                created_at=permission.created_at,
                updated_at=permission.updated_at,
            )
            result.append(item)
        return result

    @parameter_matcher(acl={aa.HasAdmin})
    async def post_permissions(self, body: CreatePermissionQ) -> None:
        if not body.name:
            raise HTTPBadRequest(reason="Not exists `name` field")
        body.normalize_booleans()
        await self.context.create_permission(
            name=body.name,
            description=body.description,
            features=body.features,
            extra=body.extra,
            r_layout=body.r_layout,
            w_layout=body.w_layout,
            r_storage=body.r_storage,
            w_storage=body.w_storage,
            r_manager=body.r_manager,
            w_manager=body.w_manager,
            r_graph=body.r_graph,
            w_graph=body.w_graph,
            r_member=body.r_member,
            w_member=body.w_member,
            r_setting=body.r_setting,
            w_setting=body.w_setting,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def get_permissions_pperm(self, perm: str) -> PermissionA:
        uid = await self.context.get_permission_uid(perm)
        db_permission = await self.context.get_permission(uid)
        assert db_permission.name is not None
        return PermissionA(
            name=db_permission.name,
            description=db_permission.description,
            features=db_permission.features,
            extra=db_permission.extra,
            r_layout=db_permission.r_layout,
            w_layout=db_permission.w_layout,
            r_storage=db_permission.r_storage,
            w_storage=db_permission.w_storage,
            r_manager=db_permission.r_manager,
            w_manager=db_permission.w_manager,
            r_graph=db_permission.r_graph,
            w_graph=db_permission.w_graph,
            r_member=db_permission.r_member,
            w_member=db_permission.w_member,
            r_setting=db_permission.r_setting,
            w_setting=db_permission.w_setting,
            created_at=db_permission.created_at,
            updated_at=db_permission.updated_at,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def patch_permissions_pperm(self, perm: str, body: UpdatePermissionQ) -> None:
        uid = await self.context.get_permission_uid(perm)
        await self.context.update_permission(
            uid,
            name=body.name,
            description=body.description,
            features=body.features,
            extra=body.extra,
            r_layout=body.r_layout,
            w_layout=body.w_layout,
            r_storage=body.r_storage,
            w_storage=body.w_storage,
            r_manager=body.r_manager,
            w_manager=body.w_manager,
            r_graph=body.r_graph,
            w_graph=body.w_graph,
            r_member=body.r_member,
            w_member=body.w_member,
            r_setting=body.r_setting,
            w_setting=body.w_setting,
        )

    @parameter_matcher(acl={aa.HasAdmin})
    async def delete_permissions_pperm(self, perm: str) -> None:
        uid = await self.context.get_permission_uid(perm)
        await self.context.delete_permission(uid)
