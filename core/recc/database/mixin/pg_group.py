# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.group import (
    DELETE_GROUP_BY_UID,
    INSERT_GROUP,
    SELECT_GROUP_ALL,
    SELECT_GROUP_BY_BELOW_VISIBILITY,
    SELECT_GROUP_BY_UID,
    SELECT_GROUP_COUNT,
    SELECT_GROUP_SLUG_BY_UID,
    SELECT_GROUP_UID_BY_SLUG,
    get_update_group_query_by_uid,
)
from recc.packet.group import Group
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


class PgGroup(PgBase):
    async def insert_group(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility=VISIBILITY_LEVEL_PRIVATE,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else tznow()
        return await self.column(
            int,
            INSERT_GROUP,
            slug,
            name,
            description,
            features,
            visibility,
            extra,
            created,
        )

    async def update_group_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility: Optional[int] = None,
        extra: Optional[Any] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        query, args = get_update_group_query_by_uid(
            uid=uid,
            slug=slug,
            name=name,
            description=description,
            features=features,
            visibility=visibility,
            extra=extra,
            updated_at=updated,
        )
        await self.execute(query, *args)

    async def delete_group_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_GROUP_BY_UID, uid)

    async def select_group_uid_by_slug(self, slug: str) -> int:
        return await self.column(int, SELECT_GROUP_UID_BY_SLUG, slug)

    async def select_group_slug_by_uid(self, uid: int) -> str:
        return await self.column(str, SELECT_GROUP_SLUG_BY_UID, uid)

    async def select_group_by_uid(self, uid: int) -> Group:
        return await self.row(Group, SELECT_GROUP_BY_UID, uid)

    async def select_groups_by_below_visibility(self, visibility: int) -> List[Group]:
        return await self.rows(Group, SELECT_GROUP_BY_BELOW_VISIBILITY, visibility)

    async def select_groups(self) -> List[Group]:
        return await self.rows(Group, SELECT_GROUP_ALL)

    async def select_groups_count(self) -> int:
        return await self.column(int, SELECT_GROUP_COUNT)
