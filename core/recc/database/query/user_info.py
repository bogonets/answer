# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_USER_INFO

INSERT_USER_INFO = f"""
INSERT INTO {TABLE_USER_INFO} (
    user_uid,
    key,
    value,
    created_at,
    updated_at
) VALUES (
    $1, $2, $3, $4, $4
);
"""

UPSERT_USER_INFO = f"""
INSERT INTO {TABLE_USER_INFO} (
    user_uid,
    key,
    value,
    created_at,
    updated_at
) VALUES (
    $1, $2, $3, $4, $4
) ON CONFLICT (
    user_uid,
    key
) DO UPDATE SET
    value=$3,
    updated_at=$4;
"""

UPDATE_USER_INFO_VALUE_BY_KEY = f"""
UPDATE {TABLE_USER_INFO}
SET value=$3, updated_at=$4
WHERE user_uid=$1 AND key=$2;
"""

DELETE_USER_INFO_BY_KEY = f"""
DELETE FROM {TABLE_USER_INFO}
WHERE user_uid=$1 AND key=$2;
"""

EXISTS_USER_INFO_BY_KEY = f"""
SELECT EXISTS (
    SELECT *
    FROM {TABLE_USER_INFO}
    WHERE user_uid=$1 AND key=$2
);
"""

SELECT_USER_INFO_UPDATED_AT_BY_KEY = f"""
SELECT updated_at
FROM {TABLE_USER_INFO}
WHERE user_uid=$1 AND key=$2;
"""

SELECT_USER_INFO_BY_KEY = f"""
SELECT *
FROM {TABLE_USER_INFO}
WHERE user_uid=$1 AND key=$2;
"""

SELECT_USER_INFO_BY_KEY_LIKE = f"""
SELECT *
FROM {TABLE_USER_INFO}
WHERE user_uid=$1 AND key LIKE $2;
"""

SELECT_USER_INFO_ALL = f"""
SELECT *
FROM {TABLE_USER_INFO}
WHERE user_uid=$1;
"""
