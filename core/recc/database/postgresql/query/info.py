# -*- coding: utf-8 -*-

from recc.variables.database import (
    TABLE_INFO,
    VIEW_INFO_DB_VERSION,
    INFO_KEY_RECC_DB_VERSION,
)
from recc.util.version import database_version

##########
# INSERT #
##########

_SAFE_INSERT_INFO_FORMAT = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at
) SELECT
    '{{key}}',
    '{{value}}',
    now()
WHERE
    NOT EXISTS(
        SELECT value
        FROM {TABLE_INFO}
        WHERE key='{{key}}'
    );
"""


def get_safe_insert_info_query(key: str, value: str) -> str:
    return _SAFE_INSERT_INFO_FORMAT.format(key=key, value=value)


SAFE_INSERT_INFO_DB_VERSION = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at
) SELECT
    '{INFO_KEY_RECC_DB_VERSION}',
    '{database_version}',
    NOW()
WHERE
    NOT EXISTS(
        SELECT value
        FROM {TABLE_INFO}
        WHERE key='{INFO_KEY_RECC_DB_VERSION}'
    );
"""

INSERT_INFO = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at
) VALUES (
    $1, $2, $3
);
"""

UPSERT_INFO = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at
) VALUES (
    $1, $2, $3
) ON CONFLICT (
    key
) DO UPDATE SET
    value=$2,
    updated_at=$3;
"""

##########
# UPDATE #
##########

UPDATE_INFO_VALUE_BY_KEY = f"""
UPDATE {TABLE_INFO}
SET value=$2, updated_at=$3
WHERE key=$1;
"""

##########
# DELETE #
##########

DELETE_INFO_BY_KEY = f"""
DELETE FROM {TABLE_INFO}
WHERE key=$1;
"""

##########
# SELECT #
##########

SELECT_INFO_BY_KEY = f"""
SELECT *
FROM {TABLE_INFO}
WHERE key=$1;
"""

SELECT_INFO_BY_KEY_LIKE = f"""
SELECT *
FROM {TABLE_INFO}
WHERE key LIKE $1;
"""

SELECT_INFO_ALL = f"""
SELECT *
FROM {TABLE_INFO};
"""

SELECT_INFO_DB_VERSION = f"""
SELECT version
FROM {VIEW_INFO_DB_VERSION};
"""
