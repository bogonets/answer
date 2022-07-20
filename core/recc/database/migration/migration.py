# -*- coding: utf-8 -*-

from asyncpg.pool import Pool

from recc.database.migration._2_1_0_to_2_2_0 import _2_1_0_to_2_2_0
from recc.util.version import SemanticVersion


async def migration_step(
    pool: Pool,
    before: SemanticVersion,
    after: SemanticVersion,
) -> None:
    if before.major == after.major and before.minor == after.minor:
        return

    if before.major == 2 and before.minor == 1:
        await _2_1_0_to_2_2_0(pool)
        await migration_step(pool, SemanticVersion(2, 2, 0), after)
