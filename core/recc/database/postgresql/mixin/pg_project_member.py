# -*- coding: utf-8 -*-

from typing import List
from overrides import overrides
from recc.database.struct.project_member import ProjectMember
from recc.database.interfaces.db_project_member import DbProjectMember
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.project_member import (
    INSERT_PROJECT_MEMBER,
    UPDATE_PROJECT_MEMBER_ROLE,
    DELETE_PROJECT_MEMBER,
    SELECT_PROJECT_MEMBER_BY_PROJECT_UID_AND_USER_UID,
    SELECT_PROJECT_MEMBER_BY_PROJECT_UID,
    SELECT_PROJECT_MEMBER_BY_USER_UID,
    SELECT_PROJECT_MEMBER_ALL,
)


class PgProjectMember(DbProjectMember, PgBase):
    @overrides
    async def insert_project_member(
        self, project_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(INSERT_PROJECT_MEMBER, project_uid, user_uid, role_uid)

    @overrides
    async def update_project_member_role(
        self, project_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(UPDATE_PROJECT_MEMBER_ROLE, project_uid, user_uid, role_uid)

    @overrides
    async def delete_project_member(self, project_uid: int, user_uid: int) -> None:
        await self.execute(DELETE_PROJECT_MEMBER, project_uid, user_uid)

    @overrides
    async def select_project_member(
        self, project_uid: int, user_uid: int
    ) -> ProjectMember:
        return await self.row(
            ProjectMember,
            SELECT_PROJECT_MEMBER_BY_PROJECT_UID_AND_USER_UID,
            project_uid,
            user_uid,
        )

    @overrides
    async def select_project_members_by_project_uid(
        self, project_uid: int
    ) -> List[ProjectMember]:
        return await self.rows(
            ProjectMember,
            SELECT_PROJECT_MEMBER_BY_PROJECT_UID,
            project_uid,
        )

    @overrides
    async def select_project_members_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectMember]:
        return await self.rows(
            ProjectMember,
            SELECT_PROJECT_MEMBER_BY_USER_UID,
            user_uid,
        )

    @overrides
    async def select_project_members(self) -> List[ProjectMember]:
        return await self.rows(ProjectMember, SELECT_PROJECT_MEMBER_ALL)
