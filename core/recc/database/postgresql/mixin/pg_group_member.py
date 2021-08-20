# -*- coding: utf-8 -*-

from typing import List
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.group_member import GroupMember
from recc.database.struct.group_join_member import GroupJoinMember
from recc.database.interfaces.db_group_member import DbGroupMember
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.group_member import (
    INSERT_GROUP_MEMBER,
    UPDATE_GROUP_MEMBER_PERMISSION,
    DELETE_GROUP_MEMBER,
    SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID,
    SELECT_GROUP_MEMBER_BY_GROUP_UID,
    SELECT_GROUP_MEMBER_BY_USER_UID,
    SELECT_GROUP_MEMBER_ALL,
    SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID,
    SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID_AND_GROUP_UID,
)


class PgGroupMember(DbGroupMember, PgBase):
    @overrides
    async def insert_group_member(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        query = INSERT_GROUP_MEMBER
        await self.execute(query, group_uid, user_uid, permission_uid)
        params_msg1 = f"group_uid={group_uid},user_uid={user_uid}"
        params_msg2 = f"permission_uid={permission_uid}"
        params_msg = f"{params_msg1},{params_msg2}"
        logger.info(f"insert_group_member({params_msg}) ok.")

    @overrides
    async def update_group_member_permission(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        query = UPDATE_GROUP_MEMBER_PERMISSION
        await self.execute(query, group_uid, user_uid, permission_uid)
        params_msg1 = f"group_uid={group_uid},user_uid={user_uid}"
        params_msg2 = f"permission_uid={permission_uid}"
        params_msg = f"{params_msg1},{params_msg2}"
        logger.info(f"update_group_member_permission({params_msg}) ok.")

    @overrides
    async def delete_group_member(self, group_uid: int, user_uid: int) -> None:
        query = DELETE_GROUP_MEMBER
        await self.execute(query, group_uid, user_uid)
        params_msg = f"group_uid={group_uid},user_uid={user_uid}"
        logger.info(f"delete_group_member({params_msg}) ok.")

    @overrides
    async def select_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        query = SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID
        row = await self.fetch_row(query, group_uid, user_uid)
        params_msg = f"group_uid={group_uid},user_uid={user_uid}"
        if not row:
            raise RuntimeError(f"Not found group member: {params_msg}")
        assert len(row) == 1
        result = GroupMember(**dict(row))
        result.group_uid = group_uid
        result.user_uid = user_uid
        logger.info(f"select_group_member({params_msg}) ok.")
        return result

    @overrides
    async def select_group_members_by_group_uid(
        self, group_uid: int
    ) -> List[GroupMember]:
        result: List[GroupMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_MEMBER_BY_GROUP_UID
                async for row in conn.cursor(query, group_uid):
                    item = GroupMember(**dict(row))
                    item.group_uid = group_uid
                    result.append(item)
        result_msg = f"{len(result)} group members"
        logger.info(f"select_group_member_by_group_uid() -> {result_msg}")
        return result

    @overrides
    async def select_group_members_by_user_uid(
        self, user_uid: int
    ) -> List[GroupMember]:
        result: List[GroupMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_MEMBER_BY_USER_UID
                async for row in conn.cursor(query, user_uid):
                    item = GroupMember(**dict(row))
                    item.user_uid = user_uid
                    result.append(item)
        result_msg = f"{len(result)} group members"
        logger.info(f"select_group_member_by_user_uid() -> {result_msg}")
        return result

    @overrides
    async def select_group_members(self) -> List[GroupMember]:
        result: List[GroupMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_MEMBER_ALL
                async for row in conn.cursor(query):
                    result.append(GroupMember(**dict(row)))
        result_msg = f"{len(result)} group members"
        logger.info(f"select_group_members() -> {result_msg}")
        return result

    @overrides
    async def select_group_members_join_group_by_user_uid(
        self, user_uid: int
    ) -> List[GroupJoinMember]:
        result: List[GroupJoinMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID
                async for row in conn.cursor(query, user_uid):
                    result.append(GroupJoinMember(**dict(row)))
        result_msg = f"{len(result)} group members"
        logger.info(f"select_group_members_join_group_by_user_uid() -> {result_msg}")
        return result

    @overrides
    async def select_group_member_join_group_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> GroupJoinMember:
        query = SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID_AND_GROUP_UID
        row = await self.fetch_row(query, user_uid, group_uid)
        params_msg = f"user_uid={user_uid},group_uid={group_uid}"
        if not row:
            raise RuntimeError(f"Not found group member: {params_msg}")
        result = GroupJoinMember(**dict(row))
        func_name = "select_group_member_join_group_by_user_uid_and_group_uid"
        logger.info(f"{func_name}({params_msg}) ok.")
        return result
