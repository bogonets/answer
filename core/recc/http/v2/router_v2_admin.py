# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPBadRequest,
    HTTPServiceUnavailable,
)
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.session.session_ex import SessionEx
from recc.http import http_urls as u
from recc.http.http_decorator import parameter_matcher
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.environment import EnvironmentA
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.info import InfoA, CreateInfoQ, UpdateInfoQ
from recc.packet.permission import PermissionA, CreatePermissionQ, UpdatePermissionQ
from recc.packet.plugin import PluginA
from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
from recc.packet.system import SystemOverviewA
from recc.packet.template import TemplateA
from recc.packet.user import UserA, UpdateUserQ, SignupQ
from recc.database.struct.group import Group
from recc.packet.cvt.project import project_to_answer
from recc.packet.cvt.permission import permission_to_answer
from recc.variables.database import INFO_KEY_RECC_ENVS_READ

INFO_KEY_RECC_ENVS_READ_HELP_MESSAGE = (
    f"Enable '{INFO_KEY_RECC_ENVS_READ}' if you want to check environment variables"
)


class RouterV2Admin:
    """
    API version 2 for administrator.
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

    @web.middleware
    async def middleware(self, request: Request, handler):
        return await handler(request)

    # noinspection PyTypeChecker
    def _routes(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
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

            # templates
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

            # plugins
            web.get(u.plugins, self.get_plugins),

            # Environments
            web.get(u.environments, self.get_environments),
        ]
        # fmt: on

    # -------
    # Configs
    # -------

    @parameter_matcher()
    async def get_configs(self) -> List[ConfigA]:
        return self.context.get_configs()

    @parameter_matcher()
    async def get_configs_pkey(self, key: str) -> ConfigA:
        try:
            return self.context.get_config(key)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher()
    async def patch_configs_pkey(self, key: str, body: UpdateConfigValueQ) -> None:
        try:
            self.context.update_config(key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    # -----
    # Infos
    # -----

    @parameter_matcher()
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

    @parameter_matcher()
    async def post_infos(self, body: CreateInfoQ) -> None:
        try:
            await self.context.create_info(body.key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher()
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

    @parameter_matcher()
    async def patch_infos_pkey(self, key: str, body: UpdateInfoQ) -> None:
        try:
            await self.context.update_info(key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher()
    async def delete_infos_pkey(self, key: str) -> None:
        await self.context.delete_info(key)

    # ------
    # System
    # ------

    @parameter_matcher()
    async def get_system_overview(self) -> SystemOverviewA:
        return await self.context.get_system_overview()

    # ---------
    # Templates
    # ---------

    @parameter_matcher()
    async def get_templates(self) -> List[TemplateA]:
        return self.context.get_template_keys()

    # -----
    # Users
    # -----

    @parameter_matcher()
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

    @parameter_matcher()
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

    @parameter_matcher()
    async def get_users_puser(self, user: str) -> UserA:
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

    @parameter_matcher()
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

    @parameter_matcher()
    async def delete_users_puser(self, user: str) -> None:
        await self.context.remove_user(user)

    # ------
    # Groups
    # ------

    @staticmethod
    def _group_to_answer(group: Group) -> GroupA:
        assert group.slug is not None
        return GroupA(
            slug=group.slug,
            name=group.name,
            description=group.description,
            features=group.features,
            visibility=group.visibility,
            extra=group.extra,
            created_at=group.created_at,
            updated_at=group.updated_at,
        )

    @parameter_matcher()
    async def get_groups(self) -> List[GroupA]:
        result = list()
        for group in await self.context.get_groups():
            result.append(self._group_to_answer(group))
        return result

    @parameter_matcher()
    async def post_groups(self, session: SessionEx, body: CreateGroupQ) -> None:
        if not body.slug:
            raise HTTPBadRequest(reason="Not exists `slug` field")
        await self.context.create_group(
            slug=body.slug,
            name=body.name,
            description=body.description,
            features=body.features,
            visibility=body.get_visibility(),
            owner_uid=session.uid,
        )

    @parameter_matcher()
    async def get_groups_pgroup(self, group: str) -> GroupA:
        group_uid = await self.context.get_group_uid(group)
        db_group = await self.context.get_group(group_uid)
        return self._group_to_answer(db_group)

    @parameter_matcher()
    async def patch_groups_pgroup(self, group: str, body: UpdateGroupQ) -> None:
        group_uid = await self.context.get_group_uid(group)
        await self.context.update_group(
            uid=group_uid,
            name=body.name,
            description=body.description,
            features=body.features,
            visibility=body.visibility,
            extra=body.extra,
        )

    @parameter_matcher()
    async def delete_groups_pgroup(self, group: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        await self.context.delete_group(group_uid)

    # --------
    # Projects
    # --------

    @parameter_matcher()
    async def get_projects(self) -> List[ProjectA]:
        result = list()
        for project in await self.context.get_projects():
            assert project.uid is not None
            assert project.group_uid is not None
            assert project.slug is not None
            group_slug = await self.context.get_group_slug(project.group_uid)
            result.append(project_to_answer(project, group_slug))
        return result

    @parameter_matcher()
    async def post_projects(self, session: SessionEx, body: CreateProjectQ) -> None:
        group_uid = await self.context.get_group_uid(body.group_slug)
        await self.context.create_project(
            group_uid=group_uid,
            slug=body.project_slug,
            name=body.name,
            description=body.description,
            features=body.features,
            visibility=body.get_visibility(),
            extra=body.extra,
            owner_uid=session.uid,
        )

    @parameter_matcher()
    async def get_projects_pgroup_pproject(self, group: str, project: str) -> ProjectA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        db_project = await self.context.get_project(project_uid)
        assert db_project.slug is not None
        assert project == db_project.slug
        return project_to_answer(db_project, group)

    @parameter_matcher()
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
            visibility=body.visibility,
            extra=body.extra,
        )

    @parameter_matcher()
    async def delete_projects_pgroup_pproject(self, group: str, project: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        await self.context.delete_project(project_uid)

    # -----------
    # Permissions
    # -----------

    @parameter_matcher()
    async def get_permissions(self) -> List[PermissionA]:
        result = list()
        for permission in await self.context.get_permissions():
            result.append(permission_to_answer(permission))
        return result

    @parameter_matcher()
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

    @parameter_matcher()
    async def get_permissions_pperm(self, perm: str) -> PermissionA:
        uid = await self.context.get_permission_uid(perm)
        db_permission = await self.context.get_permission(uid)
        return permission_to_answer(db_permission)

    @parameter_matcher()
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

    @parameter_matcher()
    async def delete_permissions_pperm(self, perm: str) -> None:
        uid = await self.context.get_permission_uid(perm)
        await self.context.delete_permission(uid)

    # -------
    # Plugins
    # -------

    @parameter_matcher()
    async def get_plugins(self) -> List[PluginA]:
        return self.context.get_plugins()

    # ------------
    # Environments
    # ------------

    @parameter_matcher()
    async def get_environments(self) -> List[EnvironmentA]:
        readable = await self.context.opt_info_bool(INFO_KEY_RECC_ENVS_READ)
        if readable:
            return self.context.get_environments()
        else:
            if self.context.config.verbose >= 1:
                logger.debug(INFO_KEY_RECC_ENVS_READ_HELP_MESSAGE)
            raise HTTPServiceUnavailable(reason="The feature has been disabled")
