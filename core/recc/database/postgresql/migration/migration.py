# -*- coding: utf-8 -*-

from asyncpg.pool import Pool
from recc.database.postgresql.migration._2_0_0_to_2_1_0 import _2_0_0_to_2_1_0
from recc.util.version import SemanticVersion


async def migration_step(
    pool: Pool,
    before: SemanticVersion,
    after: SemanticVersion,
) -> None:
    if before.major == after.major and before.minor == after.minor:
        return

    if before.major == 2 and before.minor == 0:
        await _2_0_0_to_2_1_0(pool)
        await migration_step(pool, SemanticVersion(2, 1, 0), after)
