# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.layout import Layout
from recc.database.interfaces.db_layout import DbLayout
from recc.database.postgresql.mixin.pg_base import PgBase
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
        query = INSERT_LAYOUT
        created = created_at if created_at else today()
        uid = await self.fetch_val(
            query, project_uid, name, description, extra, created
        )
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"insert_layout({params_msg}) -> {uid}")
        return uid

    @overrides
    async def update_layout_description_by_uid(
        self,
        uid: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_LAYOUT_DESCRIPTION_BY_UID
        updated = updated_at if updated_at else today()
        await self.execute(query, uid, description, updated)
        logger.info(f"update_layout_description_by_uid(uid={uid}) ok.")

    @overrides
    async def update_layout_description_by_name(
        self,
        project_uid: int,
        name: str,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_LAYOUT_DESCRIPTION_BY_PROJECT_UID_AND_NAME
        updated = updated_at if updated_at else today()
        await self.execute(query, project_uid, name, description, updated)
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"update_layout_description_by_name({params_msg}) ok.")

    @overrides
    async def update_layout_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_LAYOUT_EXTRA_BY_UID
        updated = updated_at if updated_at else today()
        await self.execute(query, uid, extra, updated)
        logger.info(f"update_layout_extra_by_uid(uid={uid}) ok.")

    @overrides
    async def update_layout_extra_by_name(
        self,
        project_uid: int,
        name: str,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_LAYOUT_EXTRA_BY_PROJECT_UID_AND_NAME
        updated = updated_at if updated_at else today()
        await self.execute(query, project_uid, name, extra, updated)
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"update_layout_extra_by_name({params_msg}) ok.")

    @overrides
    async def delete_layout_by_uid(self, uid: int) -> None:
        query = DELETE_LAYOUT_BY_UID
        await self.execute(query, uid)
        logger.info(f"delete_layout_by_uid(uid={uid}) ok.")

    @overrides
    async def delete_layout_by_name(self, project_uid: int, name: str) -> None:
        query = DELETE_LAYOUT_BY_PROJECT_UID_AND_NAME
        await self.execute(query, project_uid, name)
        params_msg = f"project_uid={project_uid},name={name}"
        logger.info(f"delete_layout_by_name({params_msg}) ok.")

    @overrides
    async def select_layout_by_uid(self, uid: int) -> Layout:
        query = SELECT_LAYOUT_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found layout: {params_msg}")
        result = Layout(**dict(row))
        result.uid = uid
        logger.info(f"select_layout_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_layout_by_name(self, project_uid: int, name: str) -> Layout:
        query = SELECT_LAYOUT_BY_PROJECT_ID_AND_NAME
        row = await self.fetch_row(query, project_uid, name)
        params_msg = f"project_uid={project_uid},name={name}"
        if not row:
            raise RuntimeError(f"Not found layout: {params_msg}")
        result = Layout(**dict(row))
        result.project_uid = project_uid
        result.name = name
        logger.info(f"select_layout_by_name({params_msg}) ok.")
        return result

    @overrides
    async def select_layout_by_project_uid(self, project_uid: int) -> List[Layout]:
        result: List[Layout] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_LAYOUT_BY_PROJECT_ID
                async for row in conn.cursor(query, project_uid):
                    item = Layout(**dict(row))
                    item.project_uid = project_uid
                    result.append(item)
        params_msg = f"project_uid={project_uid}"
        result_msg = f"{len(result)} layout"
        logger.info(f"select_layout_by_project_uid({params_msg}) -> {result_msg}")
        return result
