# -*- coding: utf-8 -*-

from recc.variables.database import (
    DEFAULT_PERMISSION_SLUGS,
    TABLE_PERMISSION,
    TABLE_ROLE_PERMISSION,
)

INSERT_PERMISSION = f"""
INSERT INTO {TABLE_PERMISSION} (
    slug,
    created_at
) VALUES (
    $1,
    $2
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

SELECT_PERMISSION_BY_ROLE_UID = f"""
SELECT *
FROM {TABLE_PERMISSION}
WHERE uid IN (
    SELECT permission_uid
    FROM {TABLE_ROLE_PERMISSION}
    WHERE role_uid=$1
);
"""

_SAFE_INSERT_PERMISSION_ONLY_SLUG_FORMAT = f"""
INSERT INTO {TABLE_PERMISSION} (
    slug,
    created_at
) SELECT
    '{{slug}}',
    NOW()
WHERE
    NOT EXISTS (
        SELECT *
        FROM {TABLE_PERMISSION}
        WHERE slug='{{slug}}'
    );
"""


def safe_insert_permission_only_slug(slug: str) -> str:
    return _SAFE_INSERT_PERMISSION_ONLY_SLUG_FORMAT.format(slug=slug)


INSERT_PERMISSION_DEFAULTS = list(
    map(lambda x: safe_insert_permission_only_slug(x), DEFAULT_PERMISSION_SLUGS)
)
