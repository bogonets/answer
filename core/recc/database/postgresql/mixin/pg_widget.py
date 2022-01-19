# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.database.struct.widget import Widget
from recc.database.interfaces.db_widget import DbWidget
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.widget import (
    INSERT_WIDGET,
    UPDATE_WIDGET_DESCRIPTION_BY_UID,
    UPDATE_WIDGET_DESCRIPTION_BY_LAYOUT_UID_AND_NAME,
    UPDATE_WIDGET_EXTRA_BY_UID,
    UPDATE_WIDGET_EXTRA_BY_LAYOUT_UID_AND_NAME,
    DELETE_WIDGET_BY_UID,
    DELETE_WIDGET_BY_LAYOUT_UID_AND_NAME,
    SELECT_WIDGET_BY_UID,
    SELECT_WIDGET_BY_LAYOUT_ID_AND_NAME,
    SELECT_WIDGET_BY_LAYOUT_ID,
)


class PgWidget(DbWidget, PgBase):
    @overrides
    async def insert_widget(
        self,
        layout_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else today()
        return await self.column(
            int,
            INSERT_WIDGET,
            layout_uid,
            name,
            description,
            extra,
            created,
        )

    @overrides
    async def update_widget_description_by_uid(
        self,
        uid: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(UPDATE_WIDGET_DESCRIPTION_BY_UID, uid, description, updated)

    @overrides
    async def update_widget_description_by_name(
        self,
        layout_uid: int,
        name: str,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(
            UPDATE_WIDGET_DESCRIPTION_BY_LAYOUT_UID_AND_NAME,
            layout_uid,
            name,
            description,
            updated,
        )

    @overrides
    async def update_widget_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(UPDATE_WIDGET_EXTRA_BY_UID, uid, extra, updated)

    @overrides
    async def update_widget_extra_by_name(
        self,
        layout_uid: int,
        name: str,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(
            UPDATE_WIDGET_EXTRA_BY_LAYOUT_UID_AND_NAME,
            layout_uid,
            name,
            extra,
            updated,
        )

    @overrides
    async def delete_widget_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_WIDGET_BY_UID, uid)

    @overrides
    async def delete_widget_by_name(self, layout_uid: int, name: str) -> None:
        await self.execute(DELETE_WIDGET_BY_LAYOUT_UID_AND_NAME, layout_uid, name)

    @overrides
    async def select_widget_by_uid(self, uid: int) -> Widget:
        return await self.row(Widget, SELECT_WIDGET_BY_UID, uid)

    @overrides
    async def select_widget_by_name(self, layout_uid: int, name: str) -> Widget:
        return await self.row(
            Widget,
            SELECT_WIDGET_BY_LAYOUT_ID_AND_NAME,
            layout_uid,
            name,
        )

    @overrides
    async def select_widget_by_layout_uid(self, layout_uid: int) -> List[Widget]:
        return await self.rows(Widget, SELECT_WIDGET_BY_LAYOUT_ID, layout_uid)
