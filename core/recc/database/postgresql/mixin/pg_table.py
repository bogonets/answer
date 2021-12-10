# -*- coding: utf-8 -*-

from functools import reduce
from overrides import overrides
from recc.database.interfaces.db_table import DbTable
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.tables import CREATE_TABLES, DROP_TABLES
from recc.database.postgresql.query.indices import CREATE_INDICES, DROP_INDICES
from recc.database.postgresql.query.views import CREATE_VIEWS, DROP_VIEWS
from recc.database.postgresql.query.info import SAFE_INSERT_INFO_DB_VERSION
from recc.database.postgresql.query.permission import (
    INSERT_PERMISSION_DEFAULTS,
    EXISTS_PERMISSION_BY_UID,
)
from recc.variables.database import PERMISSION_UID_OWNER


class PgTable(DbTable, PgBase):
    @overrides
    async def create_tables(self) -> None:
        all_create = CREATE_TABLES + CREATE_INDICES + CREATE_VIEWS
        async with self.conn() as conn:
            async with conn.transaction():
                await conn.execute(reduce(lambda x, y: x + y, all_create))
                await conn.execute(SAFE_INSERT_INFO_DB_VERSION)

                exists_owner = await conn.fetchval(
                    EXISTS_PERMISSION_BY_UID, PERMISSION_UID_OWNER
                )
                if not exists_owner:
                    for perm_query in INSERT_PERMISSION_DEFAULTS:
                        await conn.execute(perm_query)

    @overrides
    async def drop_tables(self) -> None:
        all_drop = DROP_TABLES + DROP_INDICES + DROP_VIEWS
        all_drop_reverse = all_drop[::-1]
        query = reduce(lambda x, y: x + y, all_drop_reverse)
        assert isinstance(query, str)
        await self.execute(query)
