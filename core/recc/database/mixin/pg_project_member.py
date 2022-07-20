# -*- coding: utf-8 -*-

from typing import List

from recc.database.mixin._pg_base import PgBase
from recc.database.query.project_member import (
    DELETE_PROJECT_MEMBER,
    INSERT_PROJECT_MEMBER,
    SELECT_PROJECT_MEMBER_ALL,
    SELECT_PROJECT_MEMBER_BY_PROJECT_UID,
    SELECT_PROJECT_MEMBER_BY_PROJECT_UID_AND_USER_UID,
    SELECT_PROJECT_MEMBER_BY_USER_UID,
    UPDATE_PROJECT_MEMBER_ROLE,
)
from recc.packet.project_member import ProjectMember


class PgProjectMember(PgBase):
    async def insert_project_member(
        self, project_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(INSERT_PROJECT_MEMBER, project_uid, user_uid, role_uid)

    async def update_project_member_role(
        self, project_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(UPDATE_PROJECT_MEMBER_ROLE, project_uid, user_uid, role_uid)

    async def delete_project_member(self, project_uid: int, user_uid: int) -> None:
        await self.execute(DELETE_PROJECT_MEMBER, project_uid, user_uid)

    async def select_project_member(
        self, project_uid: int, user_uid: int
    ) -> ProjectMember:
        return await self.row(
            ProjectMember,
            SELECT_PROJECT_MEMBER_BY_PROJECT_UID_AND_USER_UID,
            project_uid,
            user_uid,
        )

    async def select_project_members_by_project_uid(
        self, project_uid: int
    ) -> List[ProjectMember]:
        return await self.rows(
            ProjectMember,
            SELECT_PROJECT_MEMBER_BY_PROJECT_UID,
            project_uid,
        )

    async def select_project_members_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectMember]:
        return await self.rows(
            ProjectMember,
            SELECT_PROJECT_MEMBER_BY_USER_UID,
            user_uid,
        )

    async def select_project_members(self) -> List[ProjectMember]:
        return await self.rows(ProjectMember, SELECT_PROJECT_MEMBER_ALL)
