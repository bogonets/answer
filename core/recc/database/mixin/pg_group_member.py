# -*- coding: utf-8 -*-

from typing import List

from recc.database.mixin._pg_base import PgBase
from recc.database.query.group_member import (
    DELETE_GROUP_MEMBER,
    INSERT_GROUP_MEMBER,
    SELECT_GROUP_MEMBER_ALL,
    SELECT_GROUP_MEMBER_BY_GROUP_UID,
    SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID,
    SELECT_GROUP_MEMBER_BY_USER_UID,
    SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID,
    SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID_AND_GROUP_UID,
    SELECT_GROUP_MEMBER_JOIN_PROJECT_BY_USER_UID,
    UPDATE_GROUP_MEMBER_ROLE,
)
from recc.packet.group_join_member import GroupJoinGroupMember, ProjectJoinGroupMember
from recc.packet.group_member import GroupMember


class PgGroupMember(PgBase):
    async def insert_group_member(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(INSERT_GROUP_MEMBER, group_uid, user_uid, role_uid)

    async def update_group_member_role(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        await self.execute(UPDATE_GROUP_MEMBER_ROLE, group_uid, user_uid, role_uid)

    async def delete_group_member(self, group_uid: int, user_uid: int) -> None:
        await self.execute(DELETE_GROUP_MEMBER, group_uid, user_uid)

    async def select_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        return await self.row(
            GroupMember,
            SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID,
            group_uid,
            user_uid,
        )

    async def select_group_members_by_group_uid(
        self, group_uid: int
    ) -> List[GroupMember]:
        return await self.rows(GroupMember, SELECT_GROUP_MEMBER_BY_GROUP_UID, group_uid)

    async def select_group_members_by_user_uid(
        self, user_uid: int
    ) -> List[GroupMember]:
        return await self.rows(GroupMember, SELECT_GROUP_MEMBER_BY_USER_UID, user_uid)

    async def select_group_members(self) -> List[GroupMember]:
        return await self.rows(GroupMember, SELECT_GROUP_MEMBER_ALL)

    async def select_group_members_join_group_by_user_uid(
        self, user_uid: int
    ) -> List[GroupJoinGroupMember]:
        return await self.rows(
            GroupJoinGroupMember,
            SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID,
            user_uid,
        )

    async def select_group_member_join_group_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> GroupJoinGroupMember:
        return await self.row(
            GroupJoinGroupMember,
            SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID_AND_GROUP_UID,
            user_uid,
            group_uid,
        )

    async def select_group_members_join_project_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectJoinGroupMember]:
        return await self.rows(
            ProjectJoinGroupMember,
            SELECT_GROUP_MEMBER_JOIN_PROJECT_BY_USER_UID,
            user_uid,
        )
