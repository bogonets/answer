# -*- coding: utf-8 -*-

from asyncpg.pool import Pool
from recc.database.postgresql.migration._2_0_0_to_2_0_1 import _2_0_0_to_2_0_1
from recc.util.version import VersionTuple


async def migration_step(pool: Pool, before: VersionTuple, after: VersionTuple) -> None:
    if before == after:
        return

    if before == (2, 0, 0):
        await _2_0_0_to_2_0_1(pool)
        await migration_step(pool, (2, 0, 1), after)
