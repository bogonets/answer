# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from recc.variables.database import (
    TABLE_GROUP,
    ANONYMOUS_GROUP_SLUG,
    ANONYMOUS_GROUP_DESCRIPTION,
)
from recc.database.query_builder import UpdateBuilder, BuildResult

##########
# INSERT #
##########

SAFE_INSERT_GROUP_ANONYMOUS = f"""
INSERT INTO {TABLE_GROUP}
    (slug, description, created_at)
SELECT
    '{ANONYMOUS_GROUP_SLUG}', '{ANONYMOUS_GROUP_DESCRIPTION}', $1
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_GROUP}
        WHERE slug LIKE '{ANONYMOUS_GROUP_SLUG}'
    );
"""

INSERT_GROUP = f"""
INSERT INTO {TABLE_GROUP}
    (slug, name, description, features, extra, created_at)
VALUES
    ($1, $2, $3, $4, $5, $6);
"""

##########
# UPDATE #
##########

UPDATE_GROUP_SLUG_BY_UID = f"""
UPDATE {TABLE_GROUP}
SET slug=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_GROUP_DESCRIPTION_BY_UID = f"""
UPDATE {TABLE_GROUP}
SET description=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_GROUP_DESCRIPTION_BY_SLUG = f"""
UPDATE {TABLE_GROUP}
SET description=$2, updated_at=$3
WHERE slug LIKE $1;
"""

UPDATE_GROUP_EXTRA_BY_UID = f"""
UPDATE {TABLE_GROUP}
SET extra=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_GROUP_EXTRA_BY_SLUG = f"""
UPDATE {TABLE_GROUP}
SET extra=$2, updated_at=$3
WHERE slug LIKE $1;
"""

UPDATE_GROUP_FEATURES_BY_UID = f"""
UPDATE {TABLE_GROUP}
SET features=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_GROUP_FEATURES_BY_SLUG = f"""
UPDATE {TABLE_GROUP}
SET features=$2, updated_at=$3
WHERE slug LIKE $1;
"""


def get_update_group_query_by_uid(
    uid: int,
    slug: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    features: Optional[List[str]] = None,
    extra: Optional[Any] = None,
    updated_at=datetime.utcnow(),
) -> BuildResult:
    assert updated_at is not None
    builder = UpdateBuilder(
        if_none_skip=True,
        slug=slug,
        name=name,
        description=description,
        features=features,
        extra=extra,
        updated_at=updated_at,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_GROUP)


def get_update_group_query_by_slug(
    slug: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    features: Optional[List[str]] = None,
    extra: Optional[Any] = None,
    updated_at=datetime.utcnow(),
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
    builder.where().eq(slug=slug)
    return builder.build(TABLE_GROUP)


##########
# DELETE #
##########

DELETE_GROUP_BY_UID = f"""
DELETE FROM {TABLE_GROUP}
WHERE uid=$1;
"""

DELETE_GROUP_BY_SLUG = f"""
DELETE FROM {TABLE_GROUP}
WHERE slug LIKE $1;
"""

##########
# SELECT #
##########

SELECT_GROUP_ANONYMOUS_UID = f"""
SELECT uid
FROM {TABLE_GROUP}
WHERE slug LIKE '{ANONYMOUS_GROUP_SLUG}';
"""

SELECT_GROUP_UID_BY_SLUG = f"""
SELECT uid
FROM {TABLE_GROUP}
WHERE slug LIKE $1;
"""

SELECT_GROUP_BY_UID = f"""
SELECT *
FROM {TABLE_GROUP}
WHERE uid=$1;
"""

SELECT_GROUP_BY_SLUG = f"""
SELECT *
FROM {TABLE_GROUP}
WHERE slug LIKE $1;
"""

SELECT_GROUP_ALL = f"""
SELECT *
FROM {TABLE_GROUP};
"""

SELECT_GROUP_COUNT = f"""
SELECT
    count(uid) AS count
FROM
    {TABLE_GROUP};
"""
