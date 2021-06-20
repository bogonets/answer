# -*- coding: utf-8 -*-

from recc.variables.database import (
    TABLE_GROUP,
    ANONYMOUS_GROUP_NAME,
    ANONYMOUS_GROUP_DESCRIPTION,
)

##########
# INSERT #
##########

SAFE_INSERT_GROUP_ANONYMOUS = f"""
INSERT INTO {TABLE_GROUP}
    (name, description, created_at)
SELECT
    '{ANONYMOUS_GROUP_NAME}', '{ANONYMOUS_GROUP_DESCRIPTION}', $1
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_GROUP}
        WHERE name LIKE '{ANONYMOUS_GROUP_NAME}'
    );
"""

INSERT_GROUP = f"""
INSERT INTO {TABLE_GROUP}
    (name, description, extra, created_at)
VALUES
    ($1, $2, $3, $4);
"""

##########
# UPDATE #
##########

UPDATE_GROUP_DESCRIPTION_BY_UID = f"""
UPDATE {TABLE_GROUP}
SET description=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_GROUP_DESCRIPTION_BY_NAME = f"""
UPDATE {TABLE_GROUP}
SET description=$2, updated_at=$3
WHERE name LIKE $1;
"""

UPDATE_GROUP_EXTRA_BY_UID = f"""
UPDATE {TABLE_GROUP}
SET extra=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_GROUP_EXTRA_BY_NAME = f"""
UPDATE {TABLE_GROUP}
SET extra=$2, updated_at=$3
WHERE name LIKE $1;
"""

##########
# DELETE #
##########

DELETE_GROUP_BY_UID = f"""
DELETE FROM {TABLE_GROUP}
WHERE uid=$1;
"""

DELETE_GROUP_BY_NAME = f"""
DELETE FROM {TABLE_GROUP}
WHERE name LIKE $1;
"""

##########
# SELECT #
##########

SELECT_GROUP_ANONYMOUS_UID = f"""
SELECT uid
FROM {TABLE_GROUP}
WHERE name LIKE '{ANONYMOUS_GROUP_NAME}';
"""

SELECT_GROUP_BY_UID = f"""
SELECT name, description, extra, created_at, updated_at
FROM {TABLE_GROUP}
WHERE uid=$1;
"""

SELECT_GROUP_BY_NAME = f"""
SELECT uid, description, extra, created_at, updated_at
FROM {TABLE_GROUP}
WHERE name LIKE $1;
"""

SELECT_GROUP_ALL = f"""
SELECT uid, name, description, extra, created_at, updated_at
FROM {TABLE_GROUP};
"""
