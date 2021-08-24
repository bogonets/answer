# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_exceptions import HTTPBadRequest, HTTPForbidden
from recc.core.context import Context
from recc.http.http_decorator import parameter_matcher
from recc.session.session_ex import SessionEx
from recc.http import http_urls as u
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
from recc.packet.member import MemberA, CreateMemberQ, UpdateMemberQ
from recc.packet.permission import PermissionA
from recc.packet.cvt.project import project_to_answer
from recc.packet.cvt.group import group_to_answer
from recc.packet.cvt.permission import permission_to_answer


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
            # Permissions
            web.get(u.permissions, self.get_permissions),

            # Groups
            web.get(u.groups, self.get_groups),
            web.post(u.groups, self.post_groups),
            web.get(u.groups_pgroup, self.get_pgroup),
            web.patch(u.groups_pgroup, self.patch_pgroup),
            web.delete(u.groups_pgroup, self.delete_pgroup),

            # Group members
            web.get(u.groups_pgroup_members, self.get_groups_pgroup_members),
            web.post(u.groups_pgroup_members, self.post_groups_pgroup_members),
            web.get(u.groups_pgroup_members_pmember, self.get_groups_pgroup_members_pmember),  # noqa
            web.patch(u.groups_pgroup_members_pmember, self.patch_groups_pgroup_members_pmember),  # noqa
            web.delete(u.groups_pgroup_members_pmember, self.delete_groups_pgroup_members_pmember),  # noqa

            # Projects
            web.get(u.projects, self.get_projects),
            web.post(u.projects, self.post_projects),
            web.get(u.projects_pgroup_pproject, self.get_projects_pgroup_pproject),
            web.patch(u.projects_pgroup_pproject, self.patch_projects_pgroup_pproject),
            web.delete(u.projects_pgroup_pproject, self.delete_projects_pgroup_pproject),  # noqa

            # Project members
            web.get(u.projects_pgroup_pproject_members, self.get_projects_pgroup_pproject_members),  # noqa
            web.post(u.projects_pgroup_pproject_members, self.post_projects_pgroup_pproject_members),  # noqa
            web.get(u.projects_pgroup_pproject_members_pmember, self.get_projects_pgroup_pproject_members_pmember),  # noqa
            web.patch(u.projects_pgroup_pproject_members_pmember, self.patch_projects_pgroup_pproject_members_pmember),  # noqa
            web.delete(u.projects_pgroup_pproject_members_pmember, self.delete_projects_pgroup_pproject_members_pmember),  # noqa
        ]
        # fmt: on

    # -----------
    # Permissions
    # -----------

    @parameter_matcher()
    async def get_permissions(self) -> List[PermissionA]:
        result = list()
        for permission in await self.context.get_permissions():
            result.append(permission_to_answer(permission))
        return result

    # ------
    # Groups
    # ------

    @parameter_matcher()
    async def get_groups(self, session: SessionEx) -> List[GroupA]:
        result = list()
        for group in await self.context.get_groups_by_user(session.uid):
            result.append(group_to_answer(group))
        return result

    @parameter_matcher()
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

    @parameter_matcher()
    async def get_pgroup(self, session: SessionEx, group: str) -> GroupA:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(
            session.uid, group_uid, remove_sensitive=False
        )
        if permission.uid is None:
            raise HTTPForbidden(reason="You do not have valid permissions")
        db_group = await self.context.get_group(group_uid)
        return group_to_answer(db_group)

    @parameter_matcher()
    async def patch_pgroup(
        self, session: SessionEx, group: str, body: UpdateGroupQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(
            session.uid, group_uid, remove_sensitive=False
        )
        if permission.uid is None or not permission.w_setting:
            raise HTTPForbidden(reason="You do not have valid permissions")
        await self.context.update_group(
            uid=group_uid,
            name=body.name,
            description=body.description,
            features=body.features,
            visibility=body.visibility,
            extra=body.extra,
        )

    @parameter_matcher()
    async def delete_pgroup(self, session: SessionEx, group: str) -> None:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(
            session.uid, group_uid, remove_sensitive=False
        )
        if permission.uid is None or not permission.w_setting:
            raise HTTPForbidden(reason="You do not have valid permissions")
        await self.context.delete_group(group_uid)

    # -------------
    # Group members
    # -------------

    @parameter_matcher()
    async def get_groups_pgroup_members(
        self, session: SessionEx, group: str
    ) -> List[MemberA]:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(session.uid, group_uid)
        if not permission.r_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        members = await self.context.get_group_members(group_uid)
        result = list()
        for member in members:
            assert member.user_uid is not None
            assert member.permission_uid is not None
            username = await self.context.get_username(member.user_uid)
            permission_name = await self.context.get_permission_name(
                member.permission_uid
            )
            result.append(MemberA(username, permission_name))
        return result

    @parameter_matcher()
    async def post_groups_pgroup_members(
        self, session: SessionEx, group: str, body: CreateMemberQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(session.uid, group_uid)
        if not permission.w_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(body.username)
        member_permission_uid = await self.context.get_permission_uid(body.permission)
        await self.context.add_group_member(
            group_uid, member_user_uid, member_permission_uid
        )

    @parameter_matcher()
    async def get_groups_pgroup_members_pmember(
        self, session: SessionEx, group: str, member: str
    ) -> MemberA:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(session.uid, group_uid)
        if not permission.r_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(member)
        db_member = await self.context.get_group_member(group_uid, member_user_uid)
        assert db_member.permission_uid is not None
        member_permission_name = await self.context.get_permission_name(
            db_member.permission_uid
        )
        return MemberA(member, member_permission_name)

    @parameter_matcher()
    async def patch_groups_pgroup_members_pmember(
        self,
        session: SessionEx,
        group: str,
        member: str,
        body: UpdateMemberQ,
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(session.uid, group_uid)
        if not permission.w_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(member)
        member_permission_uid = await self.context.get_permission_uid(body.permission)
        await self.context.update_group_member(
            group_uid, member_user_uid, member_permission_uid
        )

    @parameter_matcher()
    async def delete_groups_pgroup_members_pmember(
        self, session: SessionEx, group: str, member: str
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        permission = await self.context.get_group_permission(session.uid, group_uid)
        if not permission.w_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(member)
        await self.context.remove_group_member(group_uid, member_user_uid)

    # -------
    # Project
    # -------

    @parameter_matcher()
    async def get_projects(self, session: SessionEx) -> List[ProjectA]:
        result = list()
        for project in await self.context.get_projects_by_user(
            session.uid, remove_sensitive=False
        ):
            assert project.uid is not None
            assert project.group_uid is not None
            assert project.slug is not None
            group_slug = await self.context.get_group_slug(project.group_uid)
            result.append(project_to_answer(project, group_slug))
        return result

    @parameter_matcher()
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

    @parameter_matcher()
    async def get_projects_pgroup_pproject(
        self, session: SessionEx, group: str, project: str
    ) -> ProjectA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(
            session.uid, project_uid, remove_sensitive=False
        )
        if permission.uid is None:
            raise HTTPForbidden(reason="You do not have valid permissions")

        db_project = await self.context.get_project(project_uid)
        assert db_project.slug is not None
        assert project == db_project.slug
        return project_to_answer(db_project, group)

    @parameter_matcher()
    async def patch_projects_pgroup_pproject(
        self, session: SessionEx, group: str, project: str, body: UpdateProjectQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(
            session.uid, project_uid, remove_sensitive=False
        )
        if permission.uid is None or not permission.w_setting:
            raise HTTPForbidden(reason="You do not have valid permissions")
        await self.context.update_project(
            uid=project_uid,
            name=body.name,
            description=body.description,
            features=body.features,
            visibility=body.visibility,
            extra=body.extra,
        )

    @parameter_matcher()
    async def delete_projects_pgroup_pproject(
        self, session: SessionEx, group: str, project: str
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(
            session.uid, project_uid, remove_sensitive=False
        )
        if permission.uid is None or not permission.w_setting:
            raise HTTPForbidden(reason="You do not have valid permissions")
        await self.context.delete_project(project_uid)

    # ---------------
    # Project members
    # ---------------

    @parameter_matcher()
    async def get_projects_pgroup_pproject_members(
        self, session: SessionEx, group: str, project: str
    ) -> List[MemberA]:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(session.uid, project_uid)
        if not permission.r_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        members = await self.context.get_project_members(project_uid)
        result = list()
        for member in members:
            assert member.user_uid is not None
            assert member.permission_uid is not None
            username = await self.context.get_username(member.user_uid)
            permission_name = await self.context.get_permission_name(
                member.permission_uid
            )
            result.append(MemberA(username, permission_name))
        return result

    @parameter_matcher()
    async def post_projects_pgroup_pproject_members(
        self, session: SessionEx, group: str, project: str, body: CreateMemberQ
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(session.uid, project_uid)
        if not permission.w_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(body.username)
        member_permission_uid = await self.context.get_permission_uid(body.permission)
        await self.context.add_project_member(
            project_uid, member_user_uid, member_permission_uid
        )

    @parameter_matcher()
    async def get_projects_pgroup_pproject_members_pmember(
        self, session: SessionEx, group: str, project: str, member: str
    ) -> MemberA:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(session.uid, project_uid)
        if not permission.r_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(member)
        db_member = await self.context.get_project_member(project_uid, member_user_uid)
        assert db_member.permission_uid is not None
        member_permission_name = await self.context.get_permission_name(
            db_member.permission_uid
        )
        return MemberA(member, member_permission_name)

    @parameter_matcher()
    async def patch_projects_pgroup_pproject_members_pmember(
        self,
        session: SessionEx,
        group: str,
        project: str,
        member: str,
        body: UpdateMemberQ,
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(session.uid, project_uid)
        if not permission.w_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(member)
        member_permission_uid = await self.context.get_permission_uid(body.permission)
        await self.context.update_project_member(
            project_uid, member_user_uid, member_permission_uid
        )

    @parameter_matcher()
    async def delete_projects_pgroup_pproject_members_pmember(
        self, session: SessionEx, group: str, project: str, member: str
    ) -> None:
        group_uid = await self.context.get_group_uid(group)
        project_uid = await self.context.get_project_uid(group_uid, project)
        permission = await self.context.get_project_permission(session.uid, project_uid)
        if not permission.w_member:
            raise HTTPForbidden(reason="You do not have valid permissions")

        member_user_uid = await self.context.get_user_uid(member)
        await self.context.remove_project_member(project_uid, member_user_uid)
