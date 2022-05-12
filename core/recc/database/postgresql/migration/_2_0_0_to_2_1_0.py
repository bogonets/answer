# -*- coding: utf-8 -*-

from asyncpg.pool import Pool

# [IMPORTANT]
# Do not use the database variables
# Variable values may change with version upgrades.

_MIGRATION_2_0_0_TO_2_1_0_QUERIES = """
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

-- Alter table: `recc_port`
ALTER TABLE recc_port DROP COLUMN description;
ALTER TABLE recc_port DROP COLUMN extra;
ALTER TABLE recc_port DROP CONSTRAINT recc_port_pkey;  -- remove `PRIMARY KEY`
ALTER TABLE recc_port ADD COLUMN sock INT4 NOT NULL;

-- Unique constraint `number, sock` in `recc_port` table.
ALTER TABLE recc_port
ADD CONSTRAINT recc_port_number_sock_key
UNIQUE (number, sock);

-- Alter table: `recc_daemon`
ALTER TABLE recc_daemon DROP COLUMN requirements_sha256;
ALTER TABLE recc_daemon DROP COLUMN extra;
UPDATE recc_daemon SET name='' WHERE name IS NULL;
ALTER TABLE recc_daemon ALTER COLUMN name SET NOT NULL;
ALTER TABLE recc_daemon ALTER COLUMN name SET DEFAULT '';
UPDATE recc_daemon SET address='' WHERE address IS NULL;
ALTER TABLE recc_daemon ALTER COLUMN address SET NOT NULL;
ALTER TABLE recc_daemon ALTER COLUMN address SET DEFAULT '';
UPDATE recc_daemon SET description='' WHERE description IS NULL;
ALTER TABLE recc_daemon ALTER COLUMN description SET NOT NULL;
ALTER TABLE recc_daemon ALTER COLUMN description SET DEFAULT '';

-- Create table: `recc_pip`
CREATE TABLE recc_pip (
    domain VARCHAR(128) NOT NULL DEFAULT '',
    name VARCHAR(128) NOT NULL DEFAULT '',
    file VARCHAR(256) NOT NULL DEFAULT '',
    hash_method VARCHAR(32) NOT NULL DEFAULT '',
    hash_value VARCHAR(256) NOT NULL DEFAULT ''
);

-- Update version: `2.0.0` -> `2.1.0`
UPDATE recc_info
SET value='2.1.0', updated_at=NOW()
WHERE key='recc.db.version';
"""


async def _2_0_0_to_2_1_0(pool: Pool) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(_MIGRATION_2_0_0_TO_2_1_0_QUERIES)
