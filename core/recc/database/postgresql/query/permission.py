# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_PERMISSION, DEFAULT_PERMISSION_SLUGS

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
