# -*- coding: utf-8 -*-

from typing import List
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.project_member import ProjectMember
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
from recc.database.postgresql.query.project_member import (
    INSERT_PROJECT_MEMBER,
    UPDATE_PROJECT_MEMBER_PERMISSION,
    DELETE_PROJECT_MEMBER,
    SELECT_PROJECT_MEMBER_BY_PROJECT_UID_AND_USER_UID,
    SELECT_PROJECT_MEMBER_BY_PROJECT_UID,
    SELECT_PROJECT_MEMBER_BY_USER_UID,
    SELECT_PROJECT_MEMBER_ALL,
)


class AsyncPgProjectMember(AsyncPgBase):
    async def create_project_member(
        self, project_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        query = INSERT_PROJECT_MEMBER
        await self.execute(query, project_uid, user_uid, permission_uid)
        params_msg1 = f"project_uid={project_uid},user_uid={user_uid}"
        params_msg2 = f"permission_uid={permission_uid}"
        params_msg = f"{params_msg1},{params_msg2}"
        logger.info(f"create_project_member({params_msg}) ok.")

    async def update_project_member_permission(
        self, project_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        query = UPDATE_PROJECT_MEMBER_PERMISSION
        await self.execute(query, project_uid, user_uid, permission_uid)
        params_msg1 = f"project_uid={project_uid},user_uid={user_uid}"
        params_msg2 = f"permission_uid={permission_uid}"
        params_msg = f"{params_msg1},{params_msg2}"
        logger.info(f"update_project_member_permission({params_msg}) ok.")

    async def delete_project_member(self, project_uid: int, user_uid: int) -> None:
        query = DELETE_PROJECT_MEMBER
        await self.execute(query, project_uid, user_uid)
        params_msg = f"project_uid={project_uid},user_uid={user_uid}"
        logger.info(f"delete_project_member({params_msg}) ok.")

    async def get_project_member(
        self, project_uid: int, user_uid: int
    ) -> ProjectMember:
        query = SELECT_PROJECT_MEMBER_BY_PROJECT_UID_AND_USER_UID
        row = await self.fetch_row(query, project_uid, user_uid)
        params_msg = f"project_uid={project_uid},user_uid={user_uid}"
        if not row:
            raise ReccNotFoundError(f"Not found project member: {params_msg}")
        assert len(row) == 1
        result = ProjectMember(**dict(row))
        result.project_uid = project_uid
        result.user_uid = user_uid
        logger.info(f"get_project_member({params_msg}) ok.")
        return result

    async def get_project_member_by_project_uid(
        self, project_uid: int
    ) -> List[ProjectMember]:
        result: List[ProjectMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PROJECT_MEMBER_BY_PROJECT_UID
                async for row in conn.cursor(query, project_uid):
                    item = ProjectMember(**dict(row))
                    item.project_uid = project_uid
                    result.append(item)
        result_msg = f"{len(result)} project members"
        logger.info(f"get_project_member_by_project_uid() -> {result_msg}")
        return result

    async def get_project_member_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectMember]:
        result: List[ProjectMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PROJECT_MEMBER_BY_USER_UID
                async for row in conn.cursor(query, user_uid):
                    item = ProjectMember(**dict(row))
                    item.user_uid = user_uid
                    result.append(item)
        result_msg = f"{len(result)} project members"
        logger.info(f"get_project_member_by_user_uid() -> {result_msg}")
        return result

    async def get_project_members(self) -> List[ProjectMember]:
        result: List[ProjectMember] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PROJECT_MEMBER_ALL
                async for row in conn.cursor(query):
                    result.append(ProjectMember(**dict(row)))
        result_msg = f"{len(result)} project members"
        logger.info(f"get_project_members() -> {result_msg}")
        return result
