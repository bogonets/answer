# -*- coding: utf-8 -*-

from typing import Optional, List
from datetime import datetime
from overrides import overrides
from asyncpg.exceptions import UniqueViolationError
from recc.chrono.datetime import today
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.info import Info
from recc.database.interfaces.db_info import DbInfo
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.info import (
    INSERT_INFO,
    UPDATE_INFO_VALUE_BY_KEY,
    UPSERT_INFO,
    DELETE_INFO_BY_KEY,
    EXISTS_INFO_BY_KEY,
    SELECT_INFO_BY_KEY,
    SELECT_INFO_BY_KEY_LIKE,
    SELECT_INFO_ALL,
    SELECT_INFO_DB_VERSION,
)


class PgInfo(DbInfo, PgBase):
    @overrides
    async def insert_info(
        self,
        key: str,
        value: str,
        created_at: Optional[datetime] = None,
    ) -> None:
        query = INSERT_INFO
        created = created_at if created_at else today()
        try:
            await self.execute(query, key, value, created)
        except UniqueViolationError:
            raise KeyError(f"The `{key}` key already exists")
        params_msg = f"key={key},value={value}"
        logger.info(f"insert_info({params_msg}) ok")

    @overrides
    async def update_info_value_by_key(
        self,
        key: str,
        value: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_INFO_VALUE_BY_KEY
        updated = updated_at if updated_at else today()
        await self.execute(query, key, value, updated)
        params_msg = f"key={key},value={value}"
        logger.info(f"update_info_value_by_key({params_msg}) ok.")

    @overrides
    async def upsert_info(
        self,
        key: str,
        value: str,
        created_or_updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPSERT_INFO
        time = created_or_updated_at if created_or_updated_at else today()
        await self.execute(query, key, value, time)
        params_msg = f"key={key},value={value}"
        logger.info(f"upsert_info({params_msg}) ok.")

    @overrides
    async def delete_info_by_key(self, key: str) -> None:
        query = DELETE_INFO_BY_KEY
        await self.execute(query, key)
        params_msg = f"key={key}"
        logger.info(f"delete_task_by_uid({params_msg}) ok.")

    @overrides
    async def exists_info_by_key(self, key: str) -> bool:
        query = EXISTS_INFO_BY_KEY
        result = await self.fetch_val(query, key)
        params_msg = f"key={key}"
        logger.info(f"exists_info_by_key({params_msg}) -> {result}")
        return result

    @overrides
    async def select_info_by_key(self, key: str) -> Info:
        query = SELECT_INFO_BY_KEY
        row = await self.fetch_row(query, key)
        params_msg = f"key={key}"
        if not row:
            raise RuntimeError(f"Not found info: {params_msg}")
        result = Info(**dict(row))
        result.key = key
        logger.info(f"select_info_by_key({params_msg}) ok.")
        return result

    @overrides
    async def select_infos_like(self, like: str) -> List[Info]:
        result: List[Info] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_INFO_BY_KEY_LIKE
                async for row in conn.cursor(query, like):
                    result.append(Info(**dict(row)))
        params_msg = f"like={like}"
        result_msg = f"{len(result)} infos"
        logger.info(f"select_infos_like({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def select_infos(self) -> List[Info]:
        result: List[Info] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_INFO_ALL
                async for row in conn.cursor(query):
                    result.append(Info(**dict(row)))
        result_msg = f"{len(result)} infos"
        logger.info(f"select_infos() -> {result_msg}")
        return result

    @overrides
    async def select_database_version(self) -> str:
        query = SELECT_INFO_DB_VERSION
        version = await self.fetch_val(query)
        # assert row and len(row) == 1
        # result = str(row.get("version", ""))
        logger.info(f"select_database_version() -> '{version}'")
        return version
