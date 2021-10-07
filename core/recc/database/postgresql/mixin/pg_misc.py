# -*- coding: utf-8 -*-

from functools import reduce
from datetime import datetime
from overrides import overrides
from recc.database.interfaces.db_misc import DbMisc
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.tables import CREATE_TABLES, DROP_TABLES
from recc.database.postgresql.query.indices import CREATE_INDICES, DROP_INDICES
from recc.database.postgresql.query.views import CREATE_VIEWS, DROP_VIEWS
from recc.database.postgresql.query.info import SAFE_INSERT_INFO_DB_VERSION
from recc.database.postgresql.query.group import (
    SAFE_INSERT_GROUP_ANONYMOUS,
    SELECT_GROUP_ANONYMOUS_UID,
)
from recc.database.postgresql.query.permission import (
    SAFE_INSERT_PERMISSION_DEFAULTS,
    SELECT_PERMISSION_GUEST_UID,
    SELECT_PERMISSION_REPORTER_UID,
    SELECT_PERMISSION_OPERATOR_UID,
    SELECT_PERMISSION_MAINTAINER_UID,
    SELECT_PERMISSION_OWNER_UID,
)
from recc.log.logging import recc_database_logger as logger


class PgMisc(DbMisc, PgBase):
    @overrides
    async def create_tables(self, created_at=datetime.now().astimezone()) -> None:
        all_create = CREATE_TABLES + CREATE_INDICES + CREATE_VIEWS
        async with self.conn() as conn:
            async with conn.transaction():
                await conn.execute(reduce(lambda x, y: x + y, all_create))
                await conn.execute(SAFE_INSERT_INFO_DB_VERSION, created_at)
                await conn.execute(SAFE_INSERT_GROUP_ANONYMOUS, created_at)
                for perm_query in SAFE_INSERT_PERMISSION_DEFAULTS:
                    await conn.execute(perm_query, created_at)

    @overrides
    async def drop_tables(self) -> None:
        all_drop = DROP_TABLES + DROP_INDICES + DROP_VIEWS
        all_drop_reverse = all_drop[::-1]
        await self.execute(reduce(lambda x, y: x + y, all_drop_reverse))

    async def _fetch_uid(self, query, *args, **kwargs) -> int:
        row = await self.fetch_row(query, *args, **kwargs)
        assert row and len(row) == 1
        return int(row["uid"])

    async def _get_anonymous_group_uid(self) -> int:
        return await self._fetch_uid(SELECT_GROUP_ANONYMOUS_UID)

    async def _get_guest_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_GUEST_UID)

    async def _get_reporter_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_REPORTER_UID)

    async def _get_operator_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_OPERATOR_UID)

    async def _get_maintainer_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_MAINTAINER_UID)

    async def _get_owner_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_OWNER_UID)

    @overrides
    async def update_cache(self) -> None:
        self._anonymous_group_uid = await self._get_anonymous_group_uid()
        self._guest_permission_uid = await self._get_guest_permission_uid()
        self._reporter_permission_uid = await self._get_reporter_permission_uid()
        self._operator_permission_uid = await self._get_operator_permission_uid()
        self._maintainer_permission_uid = await self._get_maintainer_permission_uid()
        self._owner_permission_uid = await self._get_owner_permission_uid()
        logger.info("PgDb.update_cache() ok.")

    @overrides
    def get_anonymous_group_uid(self) -> int:
        if self._anonymous_group_uid is None:
            raise RuntimeError("The cache has not been updated")
        return self._anonymous_group_uid

    @overrides
    def get_guest_permission_uid(self) -> int:
        if self._guest_permission_uid is None:
            raise RuntimeError("The cache has not been updated")
        return self._guest_permission_uid

    @overrides
    def get_reporter_permission_uid(self) -> int:
        if self._reporter_permission_uid is None:
            raise RuntimeError("The cache has not been updated")
        return self._reporter_permission_uid

    @overrides
    def get_operator_permission_uid(self) -> int:
        if self._operator_permission_uid is None:
            raise RuntimeError("The cache has not been updated")
        return self._operator_permission_uid

    @overrides
    def get_maintainer_permission_uid(self) -> int:
        if self._maintainer_permission_uid is None:
            raise RuntimeError("The cache has not been updated")
        return self._maintainer_permission_uid

    @overrides
    def get_owner_permission_uid(self) -> int:
        if self._owner_permission_uid is None:
            raise RuntimeError("The cache has not been updated")
        return self._owner_permission_uid
