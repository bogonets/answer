# -*- coding: utf-8 -*-

from typing import List
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.group_member import GroupMember
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
from recc.database.postgresql.query.group_member import (
    INSERT_GROUP_MEMBER,
    UPDATE_GROUP_MEMBER_PERMISSION,
    DELETE_GROUP_MEMBER,
    SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID,
    SELECT_GROUP_MEMBER_BY_GROUP_UID,
    SELECT_GROUP_MEMBER_BY_USER_UID,
    SELECT_GROUP_MEMBER_ALL,
)


class AsyncPgGroupMember(AsyncPgBase):
    async def create_group_member(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        query = INSERT_GROUP_MEMBER
        await self.execute(query, group_uid, user_uid, permission_uid)
        params_msg1 = f"group_uid={group_uid},user_uid={user_uid}"
        params_msg2 = f"permission_uid={permission_uid}"
        params_msg = f"{params_msg1},{params_msg2}"
        logger.info(f"create_group_member({params_msg}) ok.")

    async def update_group_member_permission(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        query = UPDATE_GROUP_MEMBER_PERMISSION
        await self.execute(query, group_uid, user_uid, permission_uid)
        params_msg1 = f"group_uid={group_uid},user_uid={user_uid}"
        params_msg2 = f"permission_uid={permission_uid}"
        params_msg = f"{params_msg1},{params_msg2}"
        logger.info(f"update_group_member_permission({params_msg}) ok.")

    async def delete_group_member(self, group_uid: int, user_uid: int) -> None:
        query = DELETE_GROUP_MEMBER
        await self.execute(query, group_uid, user_uid)
        params_msg = f"group_uid={group_uid},user_uid={user_uid}"
        logger.info(f"delete_group_member({params_msg}) ok.")

    async def get_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        query = SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID
        row = await self.fetch_row(query, group_uid, user_uid)
        params_msg = f"group_uid={group_uid},user_uid={user_uid}"
        if not row:
            raise ReccNotFoundError(f"Not found group member: {params_msg}")
        assert len(row) == 1
        result = GroupMember(**dict(row))
        result.group_uid = group_uid
        result.user_uid = user_uid
        logger.info(f"get_group_member({params_msg}) ok.")
        return result

    async def get_group_member_by_group_uid(self, group_uid: int) -> List[GroupMember]:
        result: List[GroupMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_MEMBER_BY_GROUP_UID
                async for row in conn.cursor(query, group_uid):
                    item = GroupMember(**dict(row))
                    item.group_uid = group_uid
                    result.append(item)
        result_msg = f"{len(result)} group members"
        logger.info(f"get_group_member_by_group_uid() -> {result_msg}")
        return result

    async def get_group_member_by_user_uid(self, user_uid: int) -> List[GroupMember]:
        result: List[GroupMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_MEMBER_BY_USER_UID
                async for row in conn.cursor(query, user_uid):
                    item = GroupMember(**dict(row))
                    item.user_uid = user_uid
                    result.append(item)
        result_msg = f"{len(result)} group members"
        logger.info(f"get_group_member_by_user_uid() -> {result_msg}")
        return result

    async def get_group_members(self) -> List[GroupMember]:
        result: List[GroupMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_MEMBER_ALL
                async for row in conn.cursor(query):
                    result.append(GroupMember(**dict(row)))
        result_msg = f"{len(result)} group members"
        logger.info(f"get_group_members() -> {result_msg}")
        return result
