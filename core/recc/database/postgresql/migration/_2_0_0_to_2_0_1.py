# -*- coding: utf-8 -*-

from asyncpg.pool import Pool

# [IMPORTANT]
# Do not use the database variables
# Variable values may change with version upgrades.

_MIGRATION_2_0_0_TO_2_0_1_QUERIES = """
-- Update all `updated_at` column, is `NOT NULL`
UPDATE recc_daemon  SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_group   SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_info    SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_layout  SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_port    SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_project SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_role    SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_task    SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_user    SET updated_at=created_at WHERE updated_at IS NULL;
UPDATE recc_widget  SET updated_at=created_at WHERE updated_at IS NULL;

-- Alter table, `updated_at` column, is `NOT NULL`
ALTER TABLE recc_daemon  ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_group   ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_info    ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_layout  ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_port    ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_project ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_role    ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_task    ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_user    ALTER COLUMN updated_at SET NOT NULL;
ALTER TABLE recc_widget  ALTER COLUMN updated_at SET NOT NULL;

-- Queries for `NOT NULL` condition in `recc_info` table.
UPDATE recc_info SET value='' WHERE value IS NULL;
ALTER TABLE recc_info ALTER COLUMN value SET NOT NULL;
ALTER TABLE recc_info ALTER COLUMN value SET DEFAULT '';

ALTER TABLE recc_port
ADD CONSTRAINT recc_port_ref_uid_ref_category_key
UNIQUE (ref_uid, ref_category);

UPDATE recc_info
SET value='2.0.1', updated_at=NOW()
WHERE key='recc.db.version';
"""


async def _2_0_0_to_2_0_1(pool: Pool) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(_MIGRATION_2_0_0_TO_2_0_1_QUERIES)
