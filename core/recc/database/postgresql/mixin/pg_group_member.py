# -*- coding: utf-8 -*-

from typing import List
from overrides import overrides
from recc.database.struct.group_member import GroupMember
from recc.database.struct.group_join_member import (
    GroupJoinGroupMember,
    ProjectJoinGroupMember,
)
from recc.database.interfaces.db_group_member import DbGroupMember
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.group_member import (
    INSERT_GROUP_MEMBER,
    UPDATE_GROUP_MEMBER_ROLE,
    DELETE_GROUP_MEMBER,
    SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID,
    SELECT_GROUP_MEMBER_BY_GROUP_UID,
    SELECT_GROUP_MEMBER_BY_USER_UID,
    SELECT_GROUP_MEMBER_ALL,
    SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID,
    SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID_AND_GROUP_UID,
    SELECT_GROUP_MEMBER_JOIN_PROJECT_BY_USER_UID,
)


class PgGroupMember(DbGroupMember, PgBase):
    @overrides
    async def insert_group_member(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(INSERT_GROUP_MEMBER, group_uid, user_uid, role_uid)

    @overrides
    async def update_group_member_role(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(UPDATE_GROUP_MEMBER_ROLE, group_uid, user_uid, role_uid)

    @overrides
    async def delete_group_member(self, group_uid: int, user_uid: int) -> None:
        await self.execute(DELETE_GROUP_MEMBER, group_uid, user_uid)

    @overrides
    async def select_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        return await self.row(
            GroupMember,
            SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID,
            group_uid,
            user_uid,
        )

    @overrides
    async def select_group_members_by_group_uid(
        self, group_uid: int
    ) -> List[GroupMember]:
        return await self.rows(GroupMember, SELECT_GROUP_MEMBER_BY_GROUP_UID, group_uid)

    @overrides
    async def select_group_members_by_user_uid(
        self, user_uid: int
    ) -> List[GroupMember]:
        return await self.rows(GroupMember, SELECT_GROUP_MEMBER_BY_USER_UID, user_uid)

    @overrides
    async def select_group_members(self) -> List[GroupMember]:
        return await self.rows(GroupMember, SELECT_GROUP_MEMBER_ALL)

    @overrides
    async def select_group_members_join_group_by_user_uid(
        self, user_uid: int
    ) -> List[GroupJoinGroupMember]:
        return await self.rows(
            GroupJoinGroupMember,
            SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID,
            user_uid,
        )

    @overrides
    async def select_group_member_join_group_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> GroupJoinGroupMember:
        return await self.row(
            GroupJoinGroupMember,
            SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID_AND_GROUP_UID,
            user_uid,
            group_uid,
        )

    @overrides
    async def select_group_members_join_project_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectJoinGroupMember]:
        return await self.rows(
            ProjectJoinGroupMember,
            SELECT_GROUP_MEMBER_JOIN_PROJECT_BY_USER_UID,
            user_uid,
        )
