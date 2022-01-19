# -*- coding: utf-8 -*-

from recc.variables.database import (
    TABLE_INFO,
    VIEW_INFO_DB_VERSION,
    INFO_KEY_RECC_DB_VERSION,
    INFO_KEY_RECC_DB_INIT,
)
from recc.util.version import database_version

INSERT_INFO_DB_VERSION = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at
) VALUES (
    '{INFO_KEY_RECC_DB_VERSION}',
    '{database_version}',
    NOW()
);
"""

INSERT_INFO_DB_INIT = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at
) VALUES (
    '{INFO_KEY_RECC_DB_INIT}',
    'True',
    NOW()
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

UPDATE_INFO_VALUE_BY_KEY = f"""
UPDATE {TABLE_INFO}
SET value=$2, updated_at=$3
WHERE key=$1;
"""

DELETE_INFO_BY_KEY = f"""
DELETE FROM {TABLE_INFO}
WHERE key=$1;
"""

EXISTS_INFO_BY_KEY = f"""
SELECT EXISTS (
    SELECT *
    FROM {TABLE_INFO}
    WHERE key=$1
);
"""

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

_SAFE_INSERT_INFO_FORMAT = f"""
INSERT INTO {TABLE_INFO} (
    key,
    value,
    created_at
) SELECT
    '{{key}}',
    '{{value}}',
    NOW()
WHERE
    NOT EXISTS(
        SELECT value
        FROM {TABLE_INFO}
        WHERE key='{{key}}'
    );
"""


def get_safe_insert_info_query(key: str, value: str) -> str:
    return _SAFE_INSERT_INFO_FORMAT.format(key=key, value=value)
