# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from recc.core.context import Context
from recc.session.session_ex import SessionEx
from recc.http.http_decorator import (
    has_member_view,
    has_member_edit,
    has_setting_edit,
    has_delete,
    domain_group,
)
from recc.http.http_parameter import parameter_matcher
from recc.http import http_urls as u
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.project import (
    ProjectA,
    CreateProjectQ,
    UpdateProjectQ,
    ProjectOverviewA,
)
from recc.packet.member import MemberA, CreateMemberQ, UpdateMemberQ
from recc.packet.role import RoleA
from recc.packet.info import InfoA
from recc.packet.cvt.project import project_to_answer
from recc.packet.cvt.group import group_to_answer
from recc.packet.cvt.role import role_to_answer


class RouterV2Main:
    """
    API version 2 for main
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
        # fmt: off
        return [
            # Groups
            web.get(u.groups, self.get_groups),
            web.post(u.groups, self.post_groups),
            web.get(u.groups_pgroup, self.get_groups_pgroup),
            web.patch(u.groups_pgroup, self.patch_groups_pgroup),
            web.delete(u.groups_pgroup, self.delete_groups_pgroup),

            # Group members
            web.get(u.groups_pgroup_members, self.get_groups_pgroup_members),
            web.post(u.groups_pgroup_members, self.post_groups_pgroup_members),
            web.get(u.groups_pgroup_members_pmember, self.get_groups_pgroup_members_pmember),  # noqa
            web.patch(u.groups_pgroup_members_pmember, self.patch_groups_pgroup_members_pmember),  # noqa
            web.delete(u.groups_pgroup_members_pmember, self.delete_groups_pgroup_members_pmember),  # noqa

            # Group projects
            web.get(u.groups_pgroup_projects, self.get_groups_pgroup_projects),

            # Projects
            web.get(u.projects, self.get_projects),
            web.post(u.projects, self.post_projects),
            web.get(u.projects_pgroup_pproject, self.get_projects_pgroup_pproject),
            web.patch(u.projects_pgroup_pproject, self.patch_projects_pgroup_pproject),
            web.delete(u.projects_pgroup_pproject, self.delete_projects_pgroup_pproject),  # noqa
            web.get(u.projects_pgroup_pproject_overview, self.get_projects_pgroup_pproject_overview),  # noqa

            # Project members
            web.get(u.projects_pgroup_pproject_members, self.get_projects_pgroup_pproject_members),  # noqa
            web.post(u.projects_pgroup_pproject_members, self.post_projects_pgroup_pproject_members),  # noqa
            web.get(u.projects_pgroup_pproject_members_pmember, self.get_projects_pgroup_pproject_members_pmember),  # noqa
            web.patch(u.projects_pgroup_pproject_members_pmember, self.patch_projects_pgroup_pproject_members_pmember),  # noqa
            web.delete(u.projects_pgroup_pproject_members_pmember, self.delete_projects_pgroup_pproject_members_pmember),  # noqa

            # Permissions
            web.get(u.permissions, self.get_permissions),

            # Roles
            web.get(u.roles, self.get_roles),
            web.get(u.roles_pgroup, self.get_roles_pgroup),
            web.get(u.roles_pgroup_pproject, self.get_roles_pgroup_pproject),

            # Users
            web.get(u.usernames, self.get_usernames),

            # Tasks
            # web.get(u.tasks_pgroup_pproject, self.get_tasks_pgroup_pproject),
            # web.patch(u.tasks_pgroup_pproject, self.patch_tasks_pgroup_pproject),

            # Infos
            web.get(u.infos_oem, self.get_infos_oem),
        ]
        # fmt: on

    # ------
    # Groups
    # ------

    @parameter_matcher
    async def get_groups(self, session: SessionEx) -> List[GroupA]:
        result = list()
        for group in await self.context.get_groups_by_user(session.uid):
            result.append(group_to_answer(group))
        return result

    @parameter_matcher
    async def post_groups(self, session: SessionEx, body: CreateGroupQ) -> None:
        if not body.slug:
            raise HTTPBadRequest(reason="Not exists `slug` field")

        # TODO: Check the maximum number of groups that can be created.

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
        return group_to_answer(db_group)

    @parameter_matcher
    @has_setting_edit
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
    @has_delete
    @domain_group
    async def delete_groups_pgroup(self, group: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        await self.context.delete_group(group_uid)

    # -------------
    # Group members
    # -------------

    @parameter_matcher
    @has_member_view
    async def get_groups_pgroup_members(self, group: str) -> List[MemberA]:
        group_uid = await self.context.get_group_uid(group)
        members = await self.context.get_group_members(group_uid)
        result = list()
        for member in members:
            assert member.user_uid is not None
            assert member.role_uid is not None
            username = await self.context.get_user_name(member.user_uid)
            role_slug = await self.context.get_role_slug(member.role_uid)
            result.append(MemberA(username, role_slug))
        return result

    @parameter_matcher
    @has_member_edit
    async def post_groups_pgroup_members(self, group: str, body: CreateMemberQ) -> None:
        group_uid = await self.context.get_group_uid(group)
        member_user_uid = await self.context.get_user_uid(body.username)
        member_role_uid = await self.context.get_role_uid(body.role)
        await self.context.add_group_member(group_uid, member_user_uid, member_role_uid)

    @parameter_matcher
    @has_member_view
    async def get_groups_pgroup_members_pmember(
        self, group: str, member: str
    ) -> MemberA:
        group_uid = await self.context.get_group_uid(group)
        member_user_uid = await self.context.get_user_uid(member)
        db_member = await self.context.get_group_member(group_uid, member_user_uid)
        assert db_member.role_uid is not None
        member_role_slug = await self.context.get_role_slug(db_member.role_uid)
        return MemberA(member, member_role_slug)

    @parameter_matcher
    @has_member_edit
    async def patch_groups_pgroup_members_pmember(
        self, group: str, member: str, body: UpdateMemberQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        member_user_uid = await self.context.get_user_uid(member)
        member_role_uid = await self.context.get_role_uid(body.role)
        await self.context.update_group_member(
            group_uid, member_user_uid, member_role_uid
        )

    @parameter_matcher
    @has_member_edit
    async def delete_groups_pgroup_members_pmember(
        self, group: str, member: str
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        member_user_uid = await self.context.get_user_uid(member)
        await self.context.remove_group_member(group_uid, member_user_uid)

    # --------------
    # Group projects
    # --------------

    @parameter_matcher
    async def get_groups_pgroup_projects(self, group: str) -> List[ProjectA]:
        group_uid = await self.context.get_group_uid(group)
        result = list()
        for project in await self.context.get_projects(group_uid):
            assert project.uid is not None
            assert project.group_uid == group_uid
            assert project.slug is not None
            result.append(project_to_answer(project, group))
        return result

    # -------
    # Project
    # -------

    @parameter_matcher
    async def get_projects(self, session: SessionEx) -> List[ProjectA]:
        result = list()
        for project in await self.context.get_projects_by_user(session.uid):
            assert project.uid is not None
            assert project.group_uid is not None
            assert project.slug is not None
            group_slug = await self.context.get_group_slug(project.group_uid)
            result.append(project_to_answer(project, group_slug))
        return result

    @parameter_matcher
    async def post_projects(self, session: SessionEx, body: CreateProjectQ) -> None:
        group_uid = await self.context.get_group_uid(body.group_slug)

        # TODO: Check the maximum number of groups that can be created.

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
    @has_setting_edit
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
    @has_setting_edit
    async def delete_projects_pgroup_pproject(self, group: str, project: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        await self.context.delete_project(project_uid)

    @parameter_matcher
    async def get_projects_pgroup_pproject_overview(
        self, group: str, project: str
    ) -> ProjectOverviewA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)

        layouts = 0
        tables = 0
        # TODO: Permission test ...
        tasks = await self.context.get_container_infos(group, project)
        members = await self.context.get_project_members(project_uid)
        return ProjectOverviewA(
            layouts=layouts,
            tables=tables,
            tasks=len(tasks),
            members=len(members),
        )

    # ---------------
    # Project members
    # ---------------

    @parameter_matcher
    @has_member_view
    async def get_projects_pgroup_pproject_members(
        self, group: str, project: str
    ) -> List[MemberA]:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        members = await self.context.get_project_members(project_uid)
        result = list()
        for member in members:
            assert member.user_uid is not None
            assert member.role_uid is not None
            username = await self.context.get_user_name(member.user_uid)
            role_slug = await self.context.get_role_slug(member.role_uid)
            result.append(MemberA(username, role_slug))
        return result

    @parameter_matcher
    @has_member_edit
    async def post_projects_pgroup_pproject_members(
        self, group: str, project: str, body: CreateMemberQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        member_user_uid = await self.context.get_user_uid(body.username)
        member_role_uid = await self.context.get_role_uid(body.role)
        await self.context.add_project_member(
            project_uid, member_user_uid, member_role_uid
        )

    @parameter_matcher
    @has_member_view
    async def get_projects_pgroup_pproject_members_pmember(
        self, group: str, project: str, member: str
    ) -> MemberA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        member_user_uid = await self.context.get_user_uid(member)
        db_member = await self.context.get_project_member(project_uid, member_user_uid)
        assert db_member.role_uid is not None
        member_role_slug = await self.context.get_role_slug(db_member.role_uid)
        return MemberA(member, member_role_slug)

    @parameter_matcher
    @has_member_edit
    async def patch_projects_pgroup_pproject_members_pmember(
        self, group: str, project: str, member: str, body: UpdateMemberQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        member_user_uid = await self.context.get_user_uid(member)
        member_role_uid = await self.context.get_role_uid(body.role)
        await self.context.update_project_member(
            project_uid, member_user_uid, member_role_uid
        )

    @parameter_matcher
    @has_member_edit
    async def delete_projects_pgroup_pproject_members_pmember(
        self, group: str, project: str, member: str
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        member_user_uid = await self.context.get_user_uid(member)
        await self.context.remove_project_member(project_uid, member_user_uid)

    # -----------
    # Permissions
    # -----------

    @parameter_matcher
    async def get_permissions(self) -> List[str]:
        perms = await self.context.get_permissions()
        result = [perm.slug for perm in perms if perm.slug]
        assert len(perms) == len(result), "Permissions with blank slugs must not exist."
        return result

    # -----
    # Roles
    # -----

    @parameter_matcher
    async def get_roles(self) -> List[RoleA]:
        return [role_to_answer(role) for role in await self.context.get_roles()]

    @parameter_matcher
    async def get_roles_pgroup(self, session: SessionEx, group: str) -> RoleA:
        group_uid = await self.context.get_group_uid(group)
        member = await self.context.get_group_member(group_uid, session.uid)
        role_uid = member.role_uid
        assert role_uid is not None
        role = await self.context.get_role(role_uid)
        return role_to_answer(role)

    @parameter_matcher
    async def get_roles_pgroup_pproject(
        self, session: SessionEx, group: str, project: str
    ) -> RoleA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        role = await self.context.get_best_role(session.uid, group_uid, project_uid)
        return role_to_answer(role)

    # -----
    # Users
    # -----

    @parameter_matcher
    async def get_usernames(self) -> List[str]:
        """
        Used from members page.
        """
        return await self.context.get_usernames()

    # -----
    # Tasks
    # -----

    # @parameter_matcher()
    # async def get_tasks_pgroup_pproject(
    #     self,
    #     session: SessionEx,
    #     group: str,
    #     project: str,
    # ) -> List[ContainerA]:
    #     group_uid = await self.context.get_group_uid(group)
    #     project_uid = await self.context.get_project_uid(group_uid, project)
    #     if not session.is_admin:
    #         role = await self.context.get_best_role(
    #             session.uid, group_uid, project_uid
    #         )
    #         if not role.r_manager:
    #             raise HTTPForbidden(reason="You do not have valid roles")
    #
    #     result = list()
    #     for container in await self.context.get_tasks(group, project):
    #         result.append(container_to_answer(container))
    #     return result
    #
    # @parameter_matcher()
    # async def patch_tasks_pgroup_pproject(
    #     self,
    #     session: SessionEx,
    #     group: str,
    #     project: str,
    #     body: ControlContainersQ,
    # ) -> None:
    #     group_uid = await self.context.get_group_uid(group)
    #     project_uid = await self.context.get_project_uid(group_uid, project)
    #     if not session.is_admin:
    #         role = await self.context.get_best_role(
    #             session.uid, group_uid, project_uid
    #         )
    #         if not role.w_manager:
    #             raise HTTPForbidden(reason="You do not have valid roles")
    #
    #     operator = ContainerOperator.from_str(body.operator)
    #     if operator == ContainerOperator.Start:
    #         for key in body.keys:
    #             await self.context.start_container(key)
    #     elif operator == ContainerOperator.Stop:
    #         for key in body.keys:
    #             await self.context.stop_container(key)
    #     elif operator == ContainerOperator.Kill:
    #         signal: Union[str, int] = body.signal if body.signal else SIGKILL
    #         for key in body.keys:
    #             await self.context.kill_container(key, signal)
    #     elif operator == ContainerOperator.Restart:
    #         for key in body.keys:
    #             await self.context.restart_container(key)
    #     elif operator == ContainerOperator.Pause:
    #         for key in body.keys:
    #             await self.context.pause_container(key)
    #     elif operator == ContainerOperator.Resume:
    #         for key in body.keys:
    #             await self.context.unpause_container(key)
    #     elif operator == ContainerOperator.Remove:
    #         force = True if body.force else False
    #         for key in body.keys:
    #             await self.context.remove_container(key, force)
    #     else:
    #         assert False, "Not accessible section"

    # -----
    # Infos
    # -----

    @parameter_matcher
    async def get_infos_oem(self) -> InfoA:
        try:
            db_info = await self.context.get_info_oem()
        except RuntimeError as e:
            raise HTTPNotFound(reason=str(e))
        assert db_info.key
        return InfoA(
            key=db_info.key,
            value=db_info.value,
            created_at=db_info.created_at,
            updated_at=db_info.updated_at,
        )
