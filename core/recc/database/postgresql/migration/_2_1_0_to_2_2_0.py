# -*- coding: utf-8 -*-

from asyncpg.pool import Pool

# [IMPORTANT]
# Do not use the database variables
# Variable values may change with version upgrades.

_MIGRATION_2_1_0_TO_2_2_0_QUERIES = """
-- Update version: `2.1.0` -> `2.2.0`
UPDATE recc_info
SET value='2.2.0', updated_at=NOW()
WHERE key='recc.db.version';
"""


async def _2_1_0_to_2_2_0(pool: Pool) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(_MIGRATION_2_1_0_TO_2_2_0_QUERIES)
