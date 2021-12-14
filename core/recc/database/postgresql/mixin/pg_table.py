# -*- coding: utf-8 -*-

from functools import reduce
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.interfaces.db_table import DbTable
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.tables import CREATE_TABLES, DROP_TABLES
from recc.database.postgresql.query.indices import CREATE_INDICES, DROP_INDICES
from recc.database.postgresql.query.views import CREATE_VIEWS, DROP_VIEWS
from recc.database.postgresql.query.info import (
    INSERT_INFO_DB_VERSION,
    INSERT_INFO_DB_INIT,
    EXISTS_INFO_BY_KEY,
    SELECT_INFO_BY_KEY,
)
from recc.database.postgresql.query.role import INSERT_ROLE_DEFAULTS
from recc.database.postgresql.query.permission import INSERT_PERMISSION_DEFAULTS
from recc.database.struct.info import Info
from recc.variables.database import INFO_KEY_RECC_DB_INIT


class PgTable(DbTable, PgBase):
    @overrides
    async def create_tables(self) -> None:
        async with self.conn() as conn:
            async with conn.transaction():
                create_tables = reduce(lambda x, y: x + y, CREATE_TABLES)
                await conn.execute(create_tables)

                create_indices = reduce(lambda x, y: x + y, CREATE_INDICES)
                await conn.execute(create_indices)

                create_views = reduce(lambda x, y: x + y, CREATE_VIEWS)
                await conn.execute(create_views)

                init_key = INFO_KEY_RECC_DB_INIT
                is_init = await conn.fetchval(EXISTS_INFO_BY_KEY, init_key)
                if is_init:
                    init_record = await conn.fetchrow(SELECT_INFO_BY_KEY, init_key)
                    init_info = Info(**dict(init_record))
                    logger.info(f"Already database initialized: {init_info.created_at}")
                    return

                insert_perms = reduce(lambda x, y: x + y, INSERT_PERMISSION_DEFAULTS)
                await conn.execute(insert_perms)

                insert_roles = reduce(lambda x, y: x + y, INSERT_ROLE_DEFAULTS)
                await conn.execute(insert_roles)

                await conn.execute(INSERT_INFO_DB_VERSION)
                await conn.execute(INSERT_INFO_DB_INIT)

    @overrides
    async def drop_tables(self) -> None:
        all_drop = DROP_TABLES + DROP_INDICES + DROP_VIEWS
        all_drop_reverse = all_drop[::-1]
        queries = reduce(lambda x, y: x + y, all_drop_reverse)
        assert isinstance(queries, str)
        await self.execute(queries)
