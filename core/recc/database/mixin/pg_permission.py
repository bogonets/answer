# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.create.functions.appropriate_permission import (
    get_select_appropriate_permission_by_user_and_group,
    get_select_appropriate_permission_by_user_and_group_and_project,
)
from recc.database.query.permission import (
    DELETE_PERMISSION_BY_UID,
    INSERT_PERMISSION,
    SELECT_PERMISSION_ALL,
    SELECT_PERMISSION_BY_ROLE_UID,
    SELECT_PERMISSION_BY_SLUG,
    SELECT_PERMISSION_BY_UID,
    SELECT_PERMISSION_SLUG_BY_UID,
    SELECT_PERMISSION_UID_BY_SLUG,
)
from recc.packet.permission import Permission


class PgPermission(PgBase):
    async def insert_permission(
        self,
        slug: str,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else tznow()
        return await self.column(int, INSERT_PERMISSION, slug, created)

    async def delete_permission(self, uid: int) -> None:
        await self.execute(DELETE_PERMISSION_BY_UID, uid)

    async def select_permission_uid_by_slug(self, slug: str) -> int:
        return await self.column(int, SELECT_PERMISSION_UID_BY_SLUG, slug)

    async def select_permission_slug_by_uid(self, uid: int) -> str:
        return await self.column(str, SELECT_PERMISSION_SLUG_BY_UID, uid)

    async def select_permission_by_slug(self, slug: str) -> Permission:
        return await self.row(Permission, SELECT_PERMISSION_BY_SLUG, slug)

    async def select_permission_by_uid(self, uid: int) -> Permission:
        return await self.row(Permission, SELECT_PERMISSION_BY_UID, uid)

    async def select_permission_all(self) -> List[Permission]:
        return await self.rows(Permission, SELECT_PERMISSION_ALL)

    async def select_permission_by_role_uid(self, role_uid: int) -> List[Permission]:
        return await self.rows(Permission, SELECT_PERMISSION_BY_ROLE_UID, role_uid)

    async def select_appropriate_permission_by_user_and_group(
        self, user_uid: int, group_uid: int
    ) -> List[Permission]:
        query = get_select_appropriate_permission_by_user_and_group(user_uid, group_uid)
        return await self.rows(Permission, query)

    async def select_appropriate_permission_by_user_and_group_and_project(
        self, user_uid: int, group_uid: int, project_uid: int
    ) -> List[Permission]:
        query = get_select_appropriate_permission_by_user_and_group_and_project(
            user_uid, group_uid, project_uid
        )
        return await self.rows(Permission, query)
