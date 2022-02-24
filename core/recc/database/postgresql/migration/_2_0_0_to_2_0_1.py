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

_MIGRATION_DAEMON_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_DAEMON}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_GROUP_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_GROUP}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_INFO_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_INFO}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_LAYOUT_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_LAYOUT}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_PORT_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_PORT}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_PROJECT_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_PROJECT}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_ROLE_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_ROLE}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_TASK_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_TASK}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_USER_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_USER}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""

_MIGRATION_WIDGET_UPDATED_AT = f"""
UPDATE {V2_0_0_TABLE_WIDGET}
SET updated_at=created_at
WHERE updated_at IS NULL;
"""


async def _updated_at_is_not_null(conn: Connection) -> None:
    # All `updated_at` is `NOT NULL`
    updated_at_is_not_null_queries = merge_queries(
        _MIGRATION_DAEMON_UPDATED_AT,
        _MIGRATION_GROUP_UPDATED_AT,
        _MIGRATION_INFO_UPDATED_AT,
        _MIGRATION_LAYOUT_UPDATED_AT,
        _MIGRATION_PORT_UPDATED_AT,
        _MIGRATION_PROJECT_UPDATED_AT,
        _MIGRATION_ROLE_UPDATED_AT,
        _MIGRATION_TASK_UPDATED_AT,
        _MIGRATION_USER_UPDATED_AT,
        _MIGRATION_WIDGET_UPDATED_AT,
    )
    await conn.execute(updated_at_is_not_null_queries)

    # TODO: alter table ...


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
