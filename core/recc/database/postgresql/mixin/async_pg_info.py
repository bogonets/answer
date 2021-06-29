# -*- coding: utf-8 -*-

from typing import List
from datetime import datetime
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.info import Info
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
from recc.database.postgresql.query.info import (
    INSERT_INFO,
    UPDATE_INFO_VALUE_BY_KEY,
    DELETE_INFO_BY_KEY,
    SELECT_INFO_BY_KEY,
    SELECT_INFO_ALL,
    SELECT_INFO_DB_VERSION,
)


class AsyncPgInfo(AsyncPgBase):
    async def create_info(
        self,
        key: str,
        value: str,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_INFO
        await self.execute(query, key, value, created_at)
        params_msg = f"key={key},value={value}"
        logger.info(f"create_info({params_msg}) ok.")

    async def update_info_value_by_key(
        self, key: str, value: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_INFO_VALUE_BY_KEY
        await self.execute(query, key, value, updated_at)
        params_msg = f"key={key},value={value}"
        logger.info(f"update_info_value_by_key({params_msg}) ok.")

    async def delete_info_by_key(self, key: str) -> None:
        query = DELETE_INFO_BY_KEY
        await self.execute(query, key)
        params_msg = f"key={key}"
        logger.info(f"delete_task_by_uid({params_msg}) ok.")

    async def get_info_by_key(self, key: str) -> Info:
        query = SELECT_INFO_BY_KEY
        row = await self.fetch_row(query, key)
        params_msg = f"key={key}"
        if not row:
            raise ReccNotFoundError(f"Not found info: {params_msg}")
        assert len(row) == 3
        result = Info(**dict(row))
        result.key = key
        logger.info(f"get_info_by_key({params_msg}) ok.")
        return result

    async def get_infos(self) -> List[Info]:
        result: List[Info] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_INFO_ALL
                async for row in conn.cursor(query):
                    result.append(Info(**dict(row)))
        result_msg = f"{len(result)} infos"
        logger.info(f"get_infos() -> {result_msg}")
        return result

    async def get_database_version(self) -> str:
        query = SELECT_INFO_DB_VERSION
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = str(row.get("version", ""))
        logger.info(f"get_database_version() -> '{result}'")
        return result
