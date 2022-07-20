# -*- coding: utf-8 -*-

from io import StringIO
from typing import List

from recc.database.mixin._pg_base import PgBase
from recc.database.query.role_permission import (
    DELETE_ROLE_PERMISSION,
    INSERT_ROLE_PERMISSION,
    SELECT_ROLE_PERMISSION_ALL,
    SELECT_ROLE_PERMISSION_BY_ROLE_UID,
    delete_role_permission_by_role_uid,
    safe_insert_role_permission_by_slug,
)
from recc.packet.role_permission import RolePermission


class PgRolePermission(PgBase):
    async def insert_role_permission(self, role_uid: int, permission_uid: int) -> None:
        await self.execute(INSERT_ROLE_PERMISSION, role_uid, permission_uid)

    async def insert_role_permissions_by_slug(
        self, role_uid: int, permission_slugs: List[str]
    ) -> None:
        buffer = StringIO()
        for slug in permission_slugs:
            buffer.write(safe_insert_role_permission_by_slug(role_uid, slug))
        await self.execute(buffer.getvalue())

    async def delete_role_permission(self, role_uid: int, permission_uid: int) -> None:
        await self.execute(DELETE_ROLE_PERMISSION, role_uid, permission_uid)

    async def update_role_permissions_by_slug(
        self, role_uid: int, permission_slugs: List[str]
    ) -> None:
        buffer = StringIO()
        buffer.write(delete_role_permission_by_role_uid(role_uid))
        for slug in permission_slugs:
            buffer.write(safe_insert_role_permission_by_slug(role_uid, slug))
        await self.execute(buffer.getvalue())

    async def select_role_permission_all(self) -> List[RolePermission]:
        return await self.rows(RolePermission, SELECT_ROLE_PERMISSION_ALL)

    async def select_role_permission_by_role_uid(
        self, role_uid: int
    ) -> List[RolePermission]:
        return await self.rows(
            RolePermission,
            SELECT_ROLE_PERMISSION_BY_ROLE_UID,
            role_uid,
        )
