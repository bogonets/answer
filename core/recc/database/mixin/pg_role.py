# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.role import (
    DELETE_ROLE_BY_UID,
    INSERT_ROLE,
    SELECT_ROLE_ALL,
    SELECT_ROLE_BY_UID,
    SELECT_ROLE_BY_USER_UID_AND_GROUP_UID,
    SELECT_ROLE_BY_USER_UID_AND_PROJECT_UID,
    SELECT_ROLE_LOCK_BY_UID,
    SELECT_ROLE_SLUG_BY_UID,
    SELECT_ROLE_UID_BY_SLUG,
    get_update_role_query_by_uid,
)
from recc.packet.role import Role


class PgRole(PgBase):
    async def insert_role(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        hidden=False,
        lock=False,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else tznow()
        return await self.column(
            int,
            INSERT_ROLE,
            slug,
            name,
            description,
            extra,
            hidden,
            lock,
            created,
        )

    async def update_role_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        hidden: Optional[bool] = None,
        lock: Optional[bool] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query, args = get_update_role_query_by_uid(
            slug=slug,
            uid=uid,
            name=name,
            description=description,
            extra=extra,
            hidden=hidden,
            lock=lock,
            updated_at=updated_at,
        )
        await self.execute(query, *args)

    async def delete_role_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_ROLE_BY_UID, uid)

    async def select_role_uid_by_slug(self, slug: str) -> int:
        return await self.column(int, SELECT_ROLE_UID_BY_SLUG, slug)

    async def select_role_slug_by_uid(self, uid: int) -> str:
        return await self.column(str, SELECT_ROLE_SLUG_BY_UID, uid)

    async def select_role_by_uid(self, uid: int) -> Role:
        return await self.row(Role, SELECT_ROLE_BY_UID, uid)

    async def select_role_lock_by_uid(self, uid: int) -> bool:
        return await self.column(bool, SELECT_ROLE_LOCK_BY_UID, uid)

    async def select_role_all(self) -> List[Role]:
        return await self.rows(Role, SELECT_ROLE_ALL)

    async def select_role_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> Role:
        return await self.row(
            Role,
            SELECT_ROLE_BY_USER_UID_AND_GROUP_UID,
            user_uid,
            group_uid,
        )

    async def select_role_by_user_uid_and_project_uid(
        self, user_uid: int, project_uid: int
    ) -> Role:
        return await self.row(
            Role,
            SELECT_ROLE_BY_USER_UID_AND_PROJECT_UID,
            user_uid,
            project_uid,
        )
