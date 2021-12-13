# -*- coding: utf-8 -*-

from typing import Optional, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.permission import Permission
from recc.database.interfaces.db_permission import DbPermission
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.permission import (
    INSERT_PERMISSION,
    DELETE_PERMISSION_BY_UID,
    SELECT_PERMISSION_UID_BY_SLUG,
    SELECT_PERMISSION_SLUG_BY_UID,
    SELECT_PERMISSION_BY_SLUG,
    SELECT_PERMISSION_BY_UID,
    SELECT_PERMISSION_ALL,
)


class PgPermission(DbPermission, PgBase):
    @overrides
    async def insert_permission(
        self,
        slug: str,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else today()
        uid = await self.fetch_val(INSERT_PERMISSION, slug, created)
        logger.info(f"insert_permission(slug={slug}) -> {uid}")
        return uid

    @overrides
    async def delete_permission(self, uid: int) -> None:
        query = DELETE_PERMISSION_BY_UID
        await self.execute(query, uid)
        logger.info(f"delete_permission(uid={uid}) ok.")

    @overrides
    async def select_permission_uid_by_slug(self, slug: str) -> int:
        query = SELECT_PERMISSION_UID_BY_SLUG
        row = await self.fetch_row(query, slug)
        params_msg = f"slug={slug}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = int(row["uid"])
        logger.info(f"select_permission_uid_by_slug({params_msg}) -> {result}")
        return result

    @overrides
    async def select_permission_slug_by_uid(self, uid: int) -> str:
        query = SELECT_PERMISSION_SLUG_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = str(row["slug"])
        logger.info(f"select_permission_slug_by_uid({params_msg}) -> {result}")
        return result

    @overrides
    async def select_permission_by_slug(self, slug: str) -> Permission:
        query = SELECT_PERMISSION_BY_SLUG
        row = await self.fetch_row(query, slug)
        params_msg = f"slug={slug}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = Permission(**dict(row))
        logger.info(f"select_permission_by_slug({params_msg}) ok.")
        return result

    @overrides
    async def select_permission_by_uid(self, uid: int) -> Permission:
        query = SELECT_PERMISSION_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = Permission(**dict(row))
        logger.info(f"select_permission_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_permission_all(self) -> List[Permission]:
        result: List[Permission] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PERMISSION_ALL
                async for row in conn.cursor(query):
                    result.append(Permission(**dict(row)))
        result_msg = f"{len(result)} permissions"
        logger.info(f"select_permission_all() -> {result_msg}")
        return result
