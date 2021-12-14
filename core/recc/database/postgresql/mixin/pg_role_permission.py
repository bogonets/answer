# -*- coding: utf-8 -*-

from typing import List
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.role_permission import RolePermission
from recc.database.interfaces.db_role_permission import DbRolePermission
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.role_permission import (
    INSERT_ROLE_PERMISSION,
    DELETE_ROLE_PERMISSION,
    SELECT_ROLE_PERMISSION_ALL,
)


class PgRolePermission(DbRolePermission, PgBase):
    @overrides
    async def insert_role_permission(self, role_uid: int, permission_uid: int) -> None:
        await self.execute(INSERT_ROLE_PERMISSION, role_uid, permission_uid)
        params_msg = f"role_uid={role_uid},permission_uid={permission_uid}"
        logger.info(f"insert_role_permission({params_msg})")

    @overrides
    async def delete_role_permission(self, role_uid: int, permission_uid: int) -> None:
        await self.execute(DELETE_ROLE_PERMISSION, role_uid, permission_uid)
        params_msg = f"role_uid={role_uid},permission_uid={permission_uid}"
        logger.info(f"delete_role_permission({params_msg})")

    @overrides
    async def select_role_permission_all(self) -> List[RolePermission]:
        result: List[RolePermission] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_ROLE_PERMISSION_ALL
                async for row in conn.cursor(query):
                    result.append(RolePermission(**dict(row)))
        result_msg = f"{len(result)} permissions"
        logger.info(f"select_role_permission_all() -> {result_msg}")
        return result
