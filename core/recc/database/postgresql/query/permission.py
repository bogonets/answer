# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from recc.chrono.datetime import today
from recc.variables.database import TABLE_PERMISSION, DEFAULT_PERMISSION_SLUGS

INITIALIZE_ONLY_INSERT_PERMISSION_FORMAT = f"""
INSERT INTO {TABLE_PERMISSION} (
    slug,
    created_at
) SELECT
    '{{slug}}',
    '{{created_at}}'
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_PERMISSION}
        WHERE slug='{{slug}}'
    );
"""


def get_safe_insert_permission_query(
    slug: str,
    created_at: Optional[datetime] = None,
) -> str:
    created = created_at if created_at else today()
    return INITIALIZE_ONLY_INSERT_PERMISSION_FORMAT.format(
        slug=slug,
        created_at=created,
    )


INSERT_PERMISSION_DEFAULTS = list(
    map(lambda x: get_safe_insert_permission_query(x), DEFAULT_PERMISSION_SLUGS)
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
