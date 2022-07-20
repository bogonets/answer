# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from asyncpg.exceptions import UniqueViolationError

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.user_info import (
    DELETE_USER_INFO_BY_KEY,
    EXISTS_USER_INFO_BY_KEY,
    INSERT_USER_INFO,
    SELECT_USER_INFO_ALL,
    SELECT_USER_INFO_BY_KEY,
    SELECT_USER_INFO_BY_KEY_LIKE,
    UPDATE_USER_INFO_VALUE_BY_KEY,
    UPSERT_USER_INFO,
)
from recc.packet.user import UserInfo


class PgUserInfo(PgBase):
    async def insert_user_info(
        self,
        user_uid: int,
        key: str,
        value: str,
        created_at: Optional[datetime] = None,
    ) -> None:
        try:
            created = created_at if created_at else tznow()
            await self.execute(INSERT_USER_INFO, user_uid, key, value, created)
        except UniqueViolationError:
            raise KeyError(f"The `{user_uid}` user_uid and `{key}` key already exists")

    async def update_user_info_value_by_key(
        self,
        user_uid: int,
        key: str,
        value: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(UPDATE_USER_INFO_VALUE_BY_KEY, user_uid, key, value, updated)

    async def upsert_user_info(
        self,
        user_uid: int,
        key: str,
        value: str,
        created_or_updated_at: Optional[datetime] = None,
    ) -> None:
        created_or_updated = created_or_updated_at if created_or_updated_at else tznow()
        await self.execute(UPSERT_USER_INFO, user_uid, key, value, created_or_updated)

    async def delete_user_info_by_key(self, user_uid: int, key: str) -> None:
        await self.execute(DELETE_USER_INFO_BY_KEY, user_uid, key)

    async def exists_user_info_by_key(self, user_uid: int, key: str) -> bool:
        return await self.column(bool, EXISTS_USER_INFO_BY_KEY, user_uid, key)

    async def select_user_info_by_key(self, user_uid: int, key: str) -> UserInfo:
        return await self.row(UserInfo, SELECT_USER_INFO_BY_KEY, user_uid, key)

    async def select_user_infos_like(self, user_uid: int, like: str) -> List[UserInfo]:
        return await self.rows(UserInfo, SELECT_USER_INFO_BY_KEY_LIKE, user_uid, like)

    async def select_user_infos(self, user_uid: int) -> List[UserInfo]:
        return await self.rows(UserInfo, SELECT_USER_INFO_ALL, user_uid)
