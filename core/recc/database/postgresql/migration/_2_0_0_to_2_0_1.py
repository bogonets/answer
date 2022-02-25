# -*- coding: utf-8 -*-

from asyncpg.pool import Pool
from asyncpg.connection import Connection
from recc.database.query_utils import merge_queries

# [IMPORTANT]
# Do not use the database variables
# Variable values may change with version upgrades.

V2_0_0_TABLE_INFO = "recc_info"
V2_0_0_TABLE_USER = "recc_user"
V2_0_0_TABLE_GROUP = "recc_group"
V2_0_0_TABLE_PERMISSION = "recc_permission"
V2_0_0_TABLE_ROLE = "recc_role"
V2_0_0_TABLE_ROLE_PERMISSION = "recc_role_permission"
V2_0_0_TABLE_PROJECT = "recc_project"
V2_0_0_TABLE_TASK = "recc_task"
V2_0_0_TABLE_LAYOUT = "recc_layout"
V2_0_0_TABLE_WIDGET = "recc_widget"
V2_0_0_TABLE_PORT = "recc_port"
V2_0_0_TABLE_DAEMON = "recc_daemon"
V2_0_0_TABLE_GROUP_MEMBER = "recc_group_member"
V2_0_0_TABLE_PROJECT_MEMBER = "recc_project_member"

_UPDATE_UPDATED_AT_IS_NOT_NULL = f"""
UPDATE {{table}}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_ALTER_COLUMN_UPDATED_AT_NOT_NULL_FORMAT = f"""
ALTER TABLE {{table}}
ALTER COLUMN updated_at SET NOT NULL;
"""

_MIGRATION_UPDATED_AT_TABLES = (
    V2_0_0_TABLE_DAEMON,
    V2_0_0_TABLE_GROUP,
    V2_0_0_TABLE_INFO,
    V2_0_0_TABLE_LAYOUT,
    V2_0_0_TABLE_PORT,
    V2_0_0_TABLE_PROJECT,
    V2_0_0_TABLE_ROLE,
    V2_0_0_TABLE_TASK,
    V2_0_0_TABLE_USER,
    V2_0_0_TABLE_WIDGET,
)


async def _updated_at_is_not_null(conn: Connection) -> None:
    # All `updated_at` is `NOT NULL`
    queries = list()

    for t in _MIGRATION_UPDATED_AT_TABLES:
        queries.append(_UPDATE_UPDATED_AT_IS_NOT_NULL.format(table=t))
    for t in _MIGRATION_UPDATED_AT_TABLES:
        queries.append(_ALTER_COLUMN_UPDATED_AT_NOT_NULL_FORMAT.format(table=t))

    await conn.execute(merge_queries(*queries))


_UPDATE_DB_VERSION = f"""
UPDATE {V2_0_0_TABLE_INFO}
SET value='2.0.1', updated_at=NOW()
WHERE key='recc.db.version';
"""


async def _update_db_version(conn: Connection) -> None:
    await conn.execute(_UPDATE_DB_VERSION)


async def _2_0_0_to_2_0_1(pool: Pool) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await _updated_at_is_not_null(conn)
            await _update_db_version(conn)
