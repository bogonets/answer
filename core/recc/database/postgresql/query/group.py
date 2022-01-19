# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from recc.chrono.datetime import today
from recc.variables.database import TABLE_GROUP, TABLE_GROUP_MEMBER
from recc.database.query_builder import UpdateBuilder, BuildResult

INSERT_GROUP = f"""
INSERT INTO {TABLE_GROUP} (
    slug,
    name,
    description,
    features,
    visibility,
    extra,
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7
) RETURNING uid;
"""

DELETE_GROUP_BY_UID = f"""
DELETE FROM {TABLE_GROUP}
WHERE uid=$1;
"""

SAFE_DELETE_GROUP_BY_UID = f"""
BEGIN;

DELETE FROM {TABLE_GROUP_MEMBER}
WHERE group_uid=$1;

DELETE FROM {TABLE_GROUP}
WHERE uid=$1;

COMMIT;
"""

SELECT_GROUP_UID_BY_SLUG = f"""
SELECT uid
FROM {TABLE_GROUP}
WHERE slug=$1;
"""

SELECT_GROUP_SLUG_BY_UID = f"""
SELECT slug
FROM {TABLE_GROUP}
WHERE uid=$1;
"""

SELECT_GROUP_BY_UID = f"""
SELECT *
FROM {TABLE_GROUP}
WHERE uid=$1;
"""

SELECT_GROUP_BY_BELOW_VISIBILITY = f"""
SELECT *
FROM {TABLE_GROUP}
WHERE visibility>=$1;
"""

SELECT_GROUP_ALL = f"""
SELECT *
FROM {TABLE_GROUP};
"""

SELECT_GROUP_COUNT = f"""
SELECT count(uid) AS count
FROM {TABLE_GROUP};
"""


def get_update_group_query_by_uid(
    uid: int,
    slug: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    features: Optional[List[str]] = None,
    visibility: Optional[int] = None,
    extra: Optional[Any] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else today()
    builder = UpdateBuilder(
        if_none_skip=True,
        slug=slug,
        name=name,
        description=description,
        features=features,
        visibility=visibility,
        extra=extra,
        updated_at=updated,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_GROUP)
