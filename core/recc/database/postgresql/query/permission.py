# -*- coding: utf-8 -*-

from recc.variables.database import (
    TABLE_PERMISSION,
    TABLE_ROLE_PERMISSION,
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    DEFAULT_PERMISSION_SLUGS,
)

INSERT_PERMISSION = f"""
INSERT INTO {TABLE_PERMISSION} (
    slug,
    description,
    extra,
    created_at
) VALUES (
    $1,
    $2,
    $3,
    $4
) RETURNING uid;
"""

DELETE_PERMISSION_BY_UID = f"""
DELETE FROM {TABLE_PERMISSION}
WHERE uid=$1;
"""

SELECT_PERMISSION_UID_BY_SLUG = f"""
SELECT uid
FROM {TABLE_PERMISSION}
WHERE slug=$1;
"""

SELECT_PERMISSION_SLUG_BY_UID = f"""
SELECT slug
FROM {TABLE_PERMISSION}
WHERE uid=$1;
"""

SELECT_PERMISSION_BY_SLUG = f"""
SELECT *
FROM {TABLE_PERMISSION}
WHERE slug=$1;
"""

SELECT_PERMISSION_BY_UID = f"""
SELECT *
FROM {TABLE_PERMISSION}
WHERE uid=$1;
"""

SELECT_PERMISSION_ALL = f"""
SELECT *
FROM {TABLE_PERMISSION};
"""

SELECT_PERMISSION_BY_USER_AND_GROUP = f"""
WITH gm AS (
    SELECT role_uid
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1 AND group_uid=$2
), rp1 AS (
    SELECT permission_uid
    FROM {TABLE_ROLE_PERMISSION} rp2, gm
    WHERE rp2.role_uid=gm.role_uid
)
SELECT *
FROM {TABLE_PERMISSION} p, rp1
WHERE p.uid=rp1.permission_uid
"""

SELECT_PERMISSION_BY_USER_AND_PROJECT = f"""
WITH pm AS (
    SELECT role_uid
    FROM {TABLE_PROJECT_MEMBER}
    WHERE user_uid=$1 AND project_uid=$2
), rp1 AS (
    SELECT permission_uid
    FROM {TABLE_ROLE_PERMISSION} rp2, pm
    WHERE rp2.role_uid=pm.role_uid
)
SELECT *
FROM {TABLE_PERMISSION} p, rp1
WHERE p.uid=rp1.permission_uid
"""

_INSERT_PERMISSION_ONLY_SLUG_FORMAT = f"""
INSERT INTO {TABLE_PERMISSION} (
    slug,
    created_at
) VALUES (
    '{{slug}}',
    NOW()
);
"""


def _insert_permission_only_slug(slug: str) -> str:
    return _INSERT_PERMISSION_ONLY_SLUG_FORMAT.format(slug=slug)


INSERT_PERMISSION_DEFAULTS = list(
    map(lambda x: _insert_permission_only_slug(x), DEFAULT_PERMISSION_SLUGS)
)
