# -*- coding: utf-8 -*-

from recc.variables.database import (
    TABLE_INFO,
    VIEW_INFO_DB_VERSION,
    RECC_DB_VERSION_KEY,
)
from recc.util.version import database_version

##########
# INSERT #
##########

SAFE_INSERT_INFO_DB_VERSION = f"""
INSERT INTO {TABLE_INFO} (
    key, value, created_at
) SELECT '{RECC_DB_VERSION_KEY}', '{database_version}', $1
WHERE
    NOT EXISTS(
        SELECT value
        FROM {TABLE_INFO}
        WHERE key LIKE '{RECC_DB_VERSION_KEY}'
    );
"""

INSERT_INFO = f"""
INSERT INTO {TABLE_INFO}
    (key, value, created_at)
VALUES
    ($1, $2, $3);
"""

##########
# UPDATE #
##########

UPDATE_INFO_VALUE_BY_KEY = f"""
UPDATE {TABLE_INFO}
SET value=$2, updated_at=$3
WHERE key LIKE $1;
"""

##########
# DELETE #
##########

DELETE_INFO_BY_KEY = f"""
DELETE FROM {TABLE_INFO}
WHERE key LIKE $1;
"""

##########
# SELECT #
##########

SELECT_INFO_BY_KEY = f"""
SELECT value, created_at, updated_at
FROM {TABLE_INFO}
WHERE key LIKE $1;
"""

SELECT_INFO_ALL = f"""
SELECT key, value, created_at, updated_at
FROM {TABLE_INFO};
"""

SELECT_INFO_DB_VERSION = f"""
SELECT version FROM {VIEW_INFO_DB_VERSION};
"""
