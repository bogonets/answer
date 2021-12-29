# -*- coding: utf-8 -*-

from typing import List
from overrides import overrides
from io import StringIO
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.role_permission import RolePermission
from recc.database.interfaces.db_role_permission import DbRolePermission
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.role_permission import (
    INSERT_ROLE_PERMISSION,
    DELETE_ROLE_PERMISSION,
    SELECT_ROLE_PERMISSION_ALL,
    SELECT_ROLE_PERMISSION_BY_ROLE_UID,
    delete_role_permission_by_role_uid,
    insert_role_permission_by_slug,
)


class PgRolePermission(DbRolePermission, PgBase):
    @overrides
    async def insert_role_permission(self, role_uid: int, permission_uid: int) -> None:
        await self.execute(INSERT_ROLE_PERMISSION, role_uid, permission_uid)
        params_msg = f"role_uid={role_uid},permission_uid={permission_uid}"
        logger.info(f"insert_role_permission({params_msg})")

    @overrides
    async def insert_role_permissions_by_slug(
        self, role_uid: int, permission_slugs: List[str]
    ) -> None:
        query_buffer = StringIO()
        for p_slug in permission_slugs:
            query_buffer.write(insert_role_permission_by_slug(role_uid, p_slug))
        query = query_buffer.getvalue()

        await self.execute(query)
        params_msg = f"role_slug={role_uid},permission_slugs={permission_slugs}"
        logger.info(f"insert_role_permissions_by_slug({params_msg})")

    @overrides
    async def delete_role_permission(self, role_uid: int, permission_uid: int) -> None:
        await self.execute(DELETE_ROLE_PERMISSION, role_uid, permission_uid)
        params_msg = f"role_uid={role_uid},permission_uid={permission_uid}"
        logger.info(f"delete_role_permission({params_msg})")

    @overrides
    async def update_role_permissions_by_slug(
        self, role_uid: int, permission_slugs: List[str]
    ) -> None:
        query_buffer = StringIO()
        query_buffer.write(delete_role_permission_by_role_uid(role_uid))
        for p_slug in permission_slugs:
            query_buffer.write(insert_role_permission_by_slug(role_uid, p_slug))
        query = query_buffer.getvalue()

        await self.execute(query)
        params_msg = f"role_slug={role_uid},permission_slugs={permission_slugs}"
        logger.info(f"update_role_permissions_by_slug({params_msg})")

    @overrides
    async def select_role_permission_all(self) -> List[RolePermission]:
        rows = await self.fetch(SELECT_ROLE_PERMISSION_ALL)
        result = [RolePermission(**dict(row)) for row in rows]
        result_msg = f"{len(result)} permissions"
        logger.info(f"select_role_permission_all() -> {result_msg}")
        return result

    @overrides
    async def select_role_permission_by_role_uid(
        self, role_uid: int
    ) -> List[RolePermission]:
        rows = await self.fetch(SELECT_ROLE_PERMISSION_BY_ROLE_UID, role_uid)
        result = [RolePermission(**dict(row)) for row in rows]
        result_msg = f"{len(result)} permissions"
        logger.info(f"select_role_permission_by_role_uid() -> {result_msg}")
        return result
