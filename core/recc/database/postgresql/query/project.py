# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional
from recc.variables.database import (
    TABLE_PROJECT,
    TABLE_PROJECT_MEMBER,
    TABLE_GROUP_MEMBER,
)
from recc.database.query_builder import UpdateBuilder, BuildResult

INSERT_PROJECT = f"""
INSERT INTO {TABLE_PROJECT} (
    group_uid,
    slug,
    name,
    description,
    features,
    visibility,
    extra,
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8
) RETURNING uid;
"""

DELETE_PROJECT_BY_UID = f"""
DELETE FROM {TABLE_PROJECT}
WHERE uid=$1;
"""

SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG = f"""
SELECT uid
FROM {TABLE_PROJECT}
WHERE group_uid=$1 AND slug=$2;
"""

SELECT_PROJECT_BY_UID = f"""
SELECT *
FROM {TABLE_PROJECT}
WHERE uid=$1;
"""

SELECT_PROJECT_BY_GROUP_ID = f"""
SELECT *
FROM {TABLE_PROJECT}
WHERE group_uid=$1;
"""

SELECT_PROJECT_BY_BELOW_VISIBILITY = f"""
SELECT *
FROM {TABLE_PROJECT}
WHERE visibility>=$1;
"""

SELECT_PROJECT_ALL = f"""
SELECT *
FROM {TABLE_PROJECT};
"""

SELECT_PROJECT_COUNT = f"""
SELECT count(uid) AS count
FROM {TABLE_PROJECT};
"""

SELECT_PROJECT_BY_USER_UID = f"""
SELECT *
FROM {TABLE_PROJECT}
WHERE uid IN (
        SELECT project_uid
        FROM {TABLE_PROJECT_MEMBER}
        WHERE user_uid=$1
    ) OR group_uid IN (
        SELECT group_uid
        FROM {TABLE_GROUP_MEMBER}
        WHERE user_uid=$1
    )
GROUP BY uid;
"""


def get_update_project_query_by_uid(
    uid: Optional[int] = None,
    slug: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    features: Optional[List[str]] = None,
    visibility: Optional[int] = None,
    extra: Optional[Any] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    assert updated_at is not None
    builder = UpdateBuilder(
        if_none_skip=True,
        slug=slug,
        name=name,
        description=description,
        features=features,
        visibility=visibility,
        extra=extra,
        updated_at=updated_at,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_PROJECT)
