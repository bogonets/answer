# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional
from recc.variables.database import TABLE_PROJECT
from recc.database.query_builder import UpdateBuilder, BuildResult


##########
# INSERT #
##########

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

##########
# UPDATE #
##########


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


##########
# DELETE #
##########

DELETE_PROJECT_BY_UID = f"""
DELETE FROM {TABLE_PROJECT}
WHERE uid=$1;
"""

##########
# SELECT #
##########

SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG = f"""
SELECT uid
FROM {TABLE_PROJECT}
WHERE group_uid=$1 AND slug LIKE $2;
"""

SELECT_PROJECT_ALL = f"""
SELECT *
FROM {TABLE_PROJECT};
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

SELECT_PROJECT_COUNT = f"""
SELECT count(uid) AS count
FROM {TABLE_PROJECT};
"""
