# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional
from recc.variables.database import TABLE_GROUP, TABLE_PROJECT
from recc.database.query_builder import UpdateBuilder, BuildResult


##########
# INSERT #
##########

INSERT_PROJECT = f"""
INSERT INTO {TABLE_PROJECT}
    (group_uid, name, description, features, extra, created_at)
VALUES
    ($1, $2, $3, $4, $5, $6);
"""

##########
# UPDATE #
##########

UPDATE_PROJECT_DESCRIPTION_BY_UID = f"""
UPDATE {TABLE_PROJECT}
SET description=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_PROJECT_DESCRIPTION_BY_GROUP_UID_AND_NAME = f"""
UPDATE {TABLE_PROJECT}
SET description=$3, updated_at=$4
WHERE group_uid=$1 AND name LIKE $2;
"""

UPDATE_PROJECT_EXTRA_BY_UID = f"""
UPDATE {TABLE_PROJECT}
SET extra=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_PROJECT_EXTRA_BY_GROUP_UID_AND_NAME = f"""
UPDATE {TABLE_PROJECT}
SET extra=$3, updated_at=$4
WHERE group_uid=$1 AND name LIKE $2;
"""

UPDATE_PROJECT_FEATURES_BY_UID = f"""
UPDATE {TABLE_PROJECT}
SET features=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_PROJECT_FEATURES_BY_GROUP_UID_AND_NAME = f"""
UPDATE {TABLE_PROJECT}
SET features=$3, updated_at=$4
WHERE group_uid=$1 AND name LIKE $2;
"""


def get_update_project_query_by_uid(
    uid: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    features: Optional[List[str]] = None,
    extra: Optional[Any] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    assert updated_at is not None
    builder = UpdateBuilder(
        if_none_skip=True,
        name=name,
        description=description,
        features=features,
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

DELETE_PROJECT_BY_GROUP_UID_AND_NAME = f"""
DELETE FROM {TABLE_PROJECT}
WHERE group_uid=$1 AND name LIKE $2;
"""

##########
# SELECT #
##########

SELECT_PROJECT_BY_UID = f"""
SELECT *
FROM {TABLE_PROJECT}
WHERE uid=$1;
"""

SELECT_PROJECT_BY_GROUP_ID_AND_NAME = f"""
SELECT *
FROM {TABLE_PROJECT}
WHERE group_uid=$1 AND name LIKE $2;
"""

SELECT_PROJECT_BY_GROUP_ID = f"""
SELECT *
FROM {TABLE_PROJECT}
WHERE group_uid=$1;
"""

SELECT_PROJECT_BY_FULLPATH = f"""
SELECT p.*
FROM (SELECT uid FROM {TABLE_GROUP} WHERE slug LIKE $1) g
    LEFT JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid AND p.name LIKE $2;
"""

SELECT_PROJECT_UID_BY_FULLPATH = f"""
SELECT p.uid AS uid
FROM (SELECT uid FROM {TABLE_GROUP} WHERE slug LIKE $1) g
    LEFT JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid AND p.name LIKE $2;
"""

SELECT_PROJECT_COUNT = f"""
SELECT
    count(uid) AS count
FROM
    {TABLE_PROJECT};
"""
