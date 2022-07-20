# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from asyncpg.exceptions import UniqueViolationError

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.info import (
    DELETE_INFO_BY_KEY,
    EXISTS_INFO_BY_KEY,
    INSERT_INFO,
    SELECT_INFO_ALL,
    SELECT_INFO_BY_KEY,
    SELECT_INFO_BY_KEY_LIKE,
    SELECT_INFO_DB_VERSION,
    UPDATE_INFO_VALUE_BY_KEY,
    UPSERT_INFO,
)
from recc.packet.info import Info


class PgInfo(PgBase):
    async def insert_info(
        self,
        key: str,
        value: str,
        created_at: Optional[datetime] = None,
    ) -> None:
        try:
            created = created_at if created_at else tznow()
            await self.execute(INSERT_INFO, key, value, created)
        except UniqueViolationError:
            raise KeyError(f"The `{key}` key already exists")

    async def update_info_value_by_key(
        self,
        key: str,
        value: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(UPDATE_INFO_VALUE_BY_KEY, key, value, updated)

    async def upsert_info(
        self,
        key: str,
        value: str,
        created_or_updated_at: Optional[datetime] = None,
    ) -> None:
        created_or_updated = created_or_updated_at if created_or_updated_at else tznow()
        await self.execute(UPSERT_INFO, key, value, created_or_updated)

    async def delete_info_by_key(self, key: str) -> None:
        await self.execute(DELETE_INFO_BY_KEY, key)

    async def exists_info_by_key(self, key: str) -> bool:
        return await self.column(bool, EXISTS_INFO_BY_KEY, key)

    async def select_info_by_key(self, key: str) -> Info:
        return await self.row(Info, SELECT_INFO_BY_KEY, key)

    async def select_infos_like(self, like: str) -> List[Info]:
        return await self.rows(Info, SELECT_INFO_BY_KEY_LIKE, like)

    async def select_infos(self) -> List[Info]:
        return await self.rows(Info, SELECT_INFO_ALL)

    async def select_database_version(self) -> str:
        return await self.column(str, SELECT_INFO_DB_VERSION)
