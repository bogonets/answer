# -*- coding: utf-8 -*-

from typing import List, Union
from signal import SIGKILL
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_exceptions import HTTPBadRequest
from recc.core.context import Context
from recc.session.session_ex import SessionEx
from recc.http import http_urls as u
from recc.http.http_parameter import parameter_matcher
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.container import ContainerOperator, ContainerA, ControlContainersQ
from recc.packet.daemon import DaemonA, CreateDaemonQ, UpdateDaemonQ
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.role import RoleA, CreateRoleQ, UpdateRoleQ
from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
from recc.packet.plugin import PluginNameA
from recc.packet.system import SystemOverviewA
from recc.packet.template import TemplateA
from recc.packet.user import UserA, UpdateUserQ, SignupQ
from recc.packet.cvt.daemon import daemon_to_answer
from recc.packet.cvt.project import project_to_answer
from recc.packet.cvt.role import role_to_answer
from recc.packet.cvt.container import container_to_answer
from recc.database.struct.group import Group


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

            # system
            web.get(u.system_overview, self.get_system_overview),

            # plugin
            web.get(u.plugin_names, self.get_plugin_names),

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

            # roles
            web.get(u.roles, self.get_roles),
            web.post(u.roles, self.post_roles),
            web.get(u.roles_prole, self.get_roles_prole),
            web.patch(u.roles_prole, self.patch_roles_prole),
            web.delete(u.roles_prole, self.delete_roles_prole),

            # containers
            web.get(u.containers, self.get_containers),
            web.patch(u.containers, self.patch_containers),
            web.get(u.containers_pcontainer, self.get_containers_pcontainer),

            # daemon
            web.get(u.daemon_plugins, self.get_daemon_plugins),
            web.get(u.daemons, self.get_daemons),
            web.post(u.daemons, self.post_daemons),
            web.get(u.daemons_pdaemon, self.get_daemons_pdaemon),
            web.patch(u.daemons_pdaemon, self.patch_daemons_pdaemon),
            web.delete(u.daemons_pdaemon, self.delete_daemons_pdaemon),
            web.post(u.daemons_pdaemon_start, self.post_daemons_pdaemon_start),
            web.post(u.daemons_pdaemon_stop, self.post_daemons_pdaemon_stop),
        ]
        # fmt: on

    # -------
    # Configs
    # -------

    @parameter_matcher
    async def get_configs(self) -> List[ConfigA]:
        return self.context.get_configs(dev_mode=False)

    @parameter_matcher
    async def get_configs_pkey(self, key: str) -> ConfigA:
        try:
            return self.context.get_config(key, dev_mode=False)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher
    async def patch_configs_pkey(self, key: str, body: UpdateConfigValueQ) -> None:
        try:
            await self.context.set_config(key, body.value, dev_mode=False)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    # ------
    # System
    # ------

    @parameter_matcher
    async def get_system_overview(self) -> SystemOverviewA:
        return await self.context.get_system_overview()

    # ------
    # Plugin
    # ------

    @parameter_matcher
    async def get_plugin_names(self) -> List[PluginNameA]:
        return list(map(lambda x: PluginNameA(x), self.context.get_plugin_keys()))

    # ---------
    # Templates
    # ---------

    @parameter_matcher
    async def get_templates(self) -> List[TemplateA]:
        return self.context.get_template_keys()

    # -----
    # Users
    # -----

    @parameter_matcher
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

    @parameter_matcher
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

    @parameter_matcher
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

    @parameter_matcher
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

    @parameter_matcher
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

    @parameter_matcher
    async def get_groups(self) -> List[GroupA]:
        result = list()
        for group in await self.context.get_groups():
            result.append(self._group_to_answer(group))
        return result

    @parameter_matcher
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

    @parameter_matcher
    async def get_groups_pgroup(self, group: str) -> GroupA:
        group_uid = await self.context.get_group_uid(group)
        db_group = await self.context.get_group(group_uid)
        return self._group_to_answer(db_group)

    @parameter_matcher
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

    @parameter_matcher
    async def delete_groups_pgroup(self, group: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        await self.context.delete_group(group_uid)

    # --------
    # Projects
    # --------

    @parameter_matcher
    async def get_projects(self) -> List[ProjectA]:
        result = list()
        for project in await self.context.get_projects():
            assert project.uid is not None
            assert project.group_uid is not None
            assert project.slug is not None
            group_slug = await self.context.get_group_slug(project.group_uid)
            result.append(project_to_answer(project, group_slug))
        return result

    @parameter_matcher
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

    @parameter_matcher
    async def get_projects_pgroup_pproject(self, group: str, project: str) -> ProjectA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        db_project = await self.context.get_project(project_uid)
        assert db_project.slug is not None
        assert project == db_project.slug
        return project_to_answer(db_project, group)

    @parameter_matcher
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

    @parameter_matcher
    async def delete_projects_pgroup_pproject(self, group: str, project: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        await self.context.delete_project(project_uid)

    # -----
    # Roles
    # -----

    @parameter_matcher
    async def get_roles(self) -> List[RoleA]:
        roles = await self.context.get_roles()
        role_permissions = await self.context.get_role_permission_slugs_dict()
        result = list()
        for role in roles:
            assert role.uid is not None
            permissions = role_permissions.get(role.uid, None)
            result.append(role_to_answer(role, permissions))
        return result

    @parameter_matcher
    async def post_roles(self, body: CreateRoleQ) -> None:
        if not body.slug:
            raise HTTPBadRequest(reason="Not exists `slug` field")
        body.normalize_booleans()
        await self.context.create_role(
            slug=body.slug,
            name=body.name,
            description=body.description,
            extra=body.extra,
            hidden=body.hidden,
            lock=body.lock,
            permissions=body.permissions,
        )

    @parameter_matcher
    async def get_roles_prole(self, role: str) -> RoleA:
        role_uid = await self.context.get_role_uid(role)
        role_info = await self.context.get_role(role_uid)
        permission_slugs = await self.context.get_permission_slugs(role_uid)
        return role_to_answer(role_info, permission_slugs)

    @parameter_matcher
    async def patch_roles_prole(self, role: str, body: UpdateRoleQ) -> None:
        uid = await self.context.get_role_uid(role)
        await self.context.update_role(
            uid,
            slug=body.slug,
            name=body.name,
            description=body.description,
            extra=body.extra,
            hidden=body.hidden,
            lock=body.lock,
            permissions=body.permissions,
        )

    @parameter_matcher
    async def delete_roles_prole(self, role: str) -> None:
        uid = await self.context.get_role_uid(role)
        await self.context.delete_role(uid)

    # ----------
    # Containers
    # ----------

    @parameter_matcher
    async def get_containers(self) -> List[ContainerA]:
        result = list()
        for container in await self.context.get_containers():
            result.append(container_to_answer(container))
        return result

    @parameter_matcher
    async def patch_containers(self, body: ControlContainersQ) -> None:
        operator = ContainerOperator.from_str(body.operator)
        if operator == ContainerOperator.Start:
            for key in body.keys:
                await self.context.start_container(key)
        elif operator == ContainerOperator.Stop:
            for key in body.keys:
                await self.context.stop_container(key)
        elif operator == ContainerOperator.Kill:
            signal: Union[str, int] = body.signal if body.signal else SIGKILL
            for key in body.keys:
                await self.context.kill_container(key, signal)
        elif operator == ContainerOperator.Restart:
            for key in body.keys:
                await self.context.restart_container(key)
        elif operator == ContainerOperator.Pause:
            for key in body.keys:
                await self.context.pause_container(key)
        elif operator == ContainerOperator.Resume:
            for key in body.keys:
                await self.context.unpause_container(key)
        elif operator == ContainerOperator.Remove:
            force = True if body.force else False
            for key in body.keys:
                await self.context.remove_container(key, force)
        else:
            assert False, "Not accessible section"

    @parameter_matcher
    async def get_containers_pcontainer(self, container: str) -> ContainerA:
        return container_to_answer(await self.context.get_container(container))

    # ------
    # Daemon
    # ------

    @parameter_matcher
    async def get_daemon_plugins(self) -> List[str]:
        return self.context.get_daemon_plugins()

    @parameter_matcher
    async def get_daemons(self) -> List[DaemonA]:
        result = list()
        daemons = await self.context.get_daemons()
        for daemon in daemons:
            if not daemon.slug:
                raise RuntimeError("The `slug` of the daemon must exist.")
            answer = daemon_to_answer(daemon)
            answer.status = self.context.status(daemon.slug)
            answer.exit_code = None
            result.append(answer)
        return result

    @parameter_matcher
    async def post_daemons(self, body: CreateDaemonQ) -> None:
        await self.context.create_daemon(
            plugin=body.plugin,
            slug=body.slug,
            name=body.name,
            address=body.address,
            requirements_sha256=None,
            description=body.description,
            extra=body.extra,
            enable=body.enable,
        )

    @parameter_matcher
    async def get_daemons_pdaemon(self, daemon: str) -> DaemonA:
        db_daemon = await self.context.get_daemon_by_slug(daemon)
        if not db_daemon.slug:
            raise RuntimeError("The `slug` of the daemon must exist.")
        answer = daemon_to_answer(db_daemon)
        answer.status = self.context.status(db_daemon.slug)
        answer.exit_code = None
        return answer

    @parameter_matcher
    async def patch_daemons_pdaemon(self, daemon: str, body: UpdateDaemonQ) -> None:
        uid = await self.context.get_daemon_uid_by_slug(daemon)
        await self.context.update_daemon(
            uid=uid,
            plugin=None,
            slug=body.slug,
            name=body.name,
            address=body.address,
            requirements_sha256=None,
            description=body.description,
            extra=body.extra,
            enable=body.enable,
        )

    @parameter_matcher
    async def delete_daemons_pdaemon(self, daemon: str) -> None:
        await self.context.delete_daemon_by_slug(daemon)

    @parameter_matcher
    async def post_daemons_pdaemon_start(self, daemon: str) -> None:
        await self.context.start_daemon(daemon)

    @parameter_matcher
    async def post_daemons_pdaemon_stop(self, daemon: str) -> None:
        await self.context.stop_daemon(daemon)
