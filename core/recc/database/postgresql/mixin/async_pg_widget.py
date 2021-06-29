# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.widget import Widget
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
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


class AsyncPgWidget(AsyncPgBase):
    async def create_widget(
        self,
        layout_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_WIDGET
        await self.execute(query, layout_uid, name, description, extra, created_at)
        params_msg = f"layout_uid={layout_uid},name={name}"
        logger.info(f"create_widget({params_msg}) ok.")

    async def update_widget_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_WIDGET_DESCRIPTION_BY_UID
        await self.execute(query, uid, description, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_widget_description_by_uid({params_msg}) ok.")

    async def update_widget_description_by_name(
        self, layout_uid: int, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_WIDGET_DESCRIPTION_BY_LAYOUT_UID_AND_NAME
        await self.execute(query, layout_uid, name, description, updated_at)
        params_msg = f"layout_uid={layout_uid},name={name}"
        logger.info(f"update_widget_description_by_name({params_msg}) ok.")

    async def update_widget_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_WIDGET_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_widget_extra_by_uid({params_msg}) ok.")

    async def update_widget_extra_by_name(
        self, layout_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_WIDGET_EXTRA_BY_LAYOUT_UID_AND_NAME
        await self.execute(query, layout_uid, name, extra, updated_at)
        params_msg = f"layout_uid={layout_uid},name={name}"
        logger.info(f"update_widget_extra_by_name({params_msg}) ok.")

    async def delete_widget_by_uid(self, uid: int) -> None:
        query = DELETE_WIDGET_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_widget_by_uid({params_msg}) ok.")

    async def delete_widget_by_name(self, layout_uid: int, name: str) -> None:
        query = DELETE_WIDGET_BY_LAYOUT_UID_AND_NAME
        await self.execute(query, layout_uid, name)
        params_msg = f"layout_uid={layout_uid},name={name}"
        logger.info(f"delete_widget_by_name({params_msg}) ok.")

    async def get_widget_by_uid(self, uid: int) -> Widget:
        query = SELECT_WIDGET_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise ReccNotFoundError(f"Not found widget: {params_msg}")
        assert len(row) == 6
        result = Widget(**dict(row))
        result.uid = uid
        logger.info(f"get_widget_by_uid({params_msg}) ok.")
        return result

    async def get_widget_by_name(self, layout_uid: int, name: str) -> Widget:
        query = SELECT_WIDGET_BY_LAYOUT_ID_AND_NAME
        row = await self.fetch_row(query, layout_uid, name)
        params_msg = f"layout_uid={layout_uid},name={name}"
        if not row:
            raise ReccNotFoundError(f"Not found widget({params_msg})")
        assert len(row) == 5
        result = Widget(**dict(row))
        result.layout_uid = layout_uid
        result.name = name
        logger.info(f"get_widget_by_name({params_msg}) ok.")
        return result

    async def get_widget_by_layout_uid(self, layout_uid: int) -> List[Widget]:
        result: List[Widget] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_WIDGET_BY_LAYOUT_ID
                async for row in conn.cursor(query, layout_uid):
                    item = Widget(**dict(row))
                    item.layout_uid = layout_uid
                    result.append(item)
        params_msg = f"layout_uid={layout_uid}"
        result_msg = f"{len(result)} widget"
        logger.info(f"get_widget_by_layout_uid({params_msg}) -> {result_msg}")
        return result
