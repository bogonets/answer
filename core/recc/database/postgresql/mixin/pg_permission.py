# -*- coding: utf-8 -*-

from typing import Optional, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.database.struct.permission import Permission
from recc.database.interfaces.db_permission import DbPermission
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.permission import (
    INSERT_PERMISSION,
    DELETE_PERMISSION_BY_UID,
    SELECT_PERMISSION_UID_BY_SLUG,
    SELECT_PERMISSION_SLUG_BY_UID,
    SELECT_PERMISSION_BY_SLUG,
    SELECT_PERMISSION_BY_UID,
    SELECT_PERMISSION_ALL,
    SELECT_PERMISSION_BY_ROLE_UID,
    SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP,
    SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_AND_PROJECT,
)


class PgPermission(DbPermission, PgBase):
    @overrides
    async def insert_permission(
        self,
        slug: str,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else today()
        return await self.column(int, INSERT_PERMISSION, slug, created)

    @overrides
    async def delete_permission(self, uid: int) -> None:
        await self.execute(DELETE_PERMISSION_BY_UID, uid)

    @overrides
    async def select_permission_uid_by_slug(self, slug: str) -> int:
        return await self.column(int, SELECT_PERMISSION_UID_BY_SLUG, slug)

    @overrides
    async def select_permission_slug_by_uid(self, uid: int) -> str:
        return await self.column(str, SELECT_PERMISSION_SLUG_BY_UID, uid)

    @overrides
    async def select_permission_by_slug(self, slug: str) -> Permission:
        return await self.row(Permission, SELECT_PERMISSION_BY_SLUG, slug)

    @overrides
    async def select_permission_by_uid(self, uid: int) -> Permission:
        return await self.row(Permission, SELECT_PERMISSION_BY_UID, uid)

    @overrides
    async def select_permission_all(self) -> List[Permission]:
        return await self.rows(Permission, SELECT_PERMISSION_ALL)

    @overrides
    async def select_permission_by_role_uid(self, role_uid: int) -> List[Permission]:
        return await self.rows(Permission, SELECT_PERMISSION_BY_ROLE_UID, role_uid)

    @overrides
    async def select_appropriate_permission_by_user_and_group(
        self, user_uid: int, group_uid: int
    ) -> List[Permission]:
        return await self.rows(
            Permission,
            SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP,
            user_uid,
            group_uid,
        )

    @overrides
    async def select_appropriate_permission_by_user_and_group_and_project(
        self, user_uid: int, group_uid: int, project_uid: int
    ) -> List[Permission]:
        return await self.rows(
            Permission,
            SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_AND_PROJECT,
            user_uid,
            group_uid,
            project_uid,
        )
