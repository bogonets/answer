# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.database.struct.layout import Layout
from recc.database.interfaces.db_layout import DbLayout
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.layout import (
    INSERT_LAYOUT,
    UPDATE_LAYOUT_DESCRIPTION_BY_UID,
    UPDATE_LAYOUT_DESCRIPTION_BY_PROJECT_UID_AND_NAME,
    UPDATE_LAYOUT_EXTRA_BY_UID,
    UPDATE_LAYOUT_EXTRA_BY_PROJECT_UID_AND_NAME,
    DELETE_LAYOUT_BY_UID,
    DELETE_LAYOUT_BY_PROJECT_UID_AND_NAME,
    SELECT_LAYOUT_BY_UID,
    SELECT_LAYOUT_BY_PROJECT_ID_AND_NAME,
    SELECT_LAYOUT_BY_PROJECT_ID,
)


class PgLayout(DbLayout, PgBase):
    @overrides
    async def insert_layout(
        self,
        project_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else today()
        return await self.column(
            int, INSERT_LAYOUT, project_uid, name, description, extra, created
        )

    @overrides
    async def update_layout_description_by_uid(
        self,
        uid: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(UPDATE_LAYOUT_DESCRIPTION_BY_UID, uid, description, updated)

    @overrides
    async def update_layout_description_by_name(
        self,
        project_uid: int,
        name: str,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(
            UPDATE_LAYOUT_DESCRIPTION_BY_PROJECT_UID_AND_NAME,
            project_uid,
            name,
            description,
            updated,
        )

    @overrides
    async def update_layout_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(UPDATE_LAYOUT_EXTRA_BY_UID, uid, extra, updated)

    @overrides
    async def update_layout_extra_by_name(
        self,
        project_uid: int,
        name: str,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(
            UPDATE_LAYOUT_EXTRA_BY_PROJECT_UID_AND_NAME,
            project_uid,
            name,
            extra,
            updated,
        )

    @overrides
    async def delete_layout_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_LAYOUT_BY_UID, uid)

    @overrides
    async def delete_layout_by_name(self, project_uid: int, name: str) -> None:
        await self.execute(DELETE_LAYOUT_BY_PROJECT_UID_AND_NAME, project_uid, name)

    @overrides
    async def select_layout_by_uid(self, uid: int) -> Layout:
        return await self.row(Layout, SELECT_LAYOUT_BY_UID, uid)

    @overrides
    async def select_layout_by_name(self, project_uid: int, name: str) -> Layout:
        return await self.row(
            Layout,
            SELECT_LAYOUT_BY_PROJECT_ID_AND_NAME,
            project_uid,
            name,
        )

    @overrides
    async def select_layout_by_project_uid(self, project_uid: int) -> List[Layout]:
        return await self.rows(Layout, SELECT_LAYOUT_BY_PROJECT_ID, project_uid)
