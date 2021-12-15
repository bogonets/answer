# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional, List
from recc.chrono.datetime import today
from recc.variables.database import (
    TABLE_ROLE,
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    ROLE_SLUG_OWNER,
    ROLE_SLUG_MAINTAINER,
    ROLE_SLUG_DEVELOPER,
    ROLE_SLUG_REPORTER,
    ROLE_SLUG_GUEST,
)
from recc.database.query_builder import UpdateBuilder, BuildResult

_INITIALIZE_ONLY_INSERT_ROLE_FORMAT = f"""
INSERT INTO {TABLE_ROLE} (
    slug,
    name,
    r_layout,
    w_layout,
    r_storage,
    w_storage,
    r_manager,
    w_manager,
    r_graph,
    w_graph,
    r_member,
    w_member,
    r_setting,
    w_setting,
    hidden,
    lock,
    created_at
) SELECT
    '{{slug}}',
    '{{name}}',
    {{r_layout}},
    {{w_layout}},
    {{r_storage}},
    {{w_storage}},
    {{r_manager}},
    {{w_manager}},
    {{r_graph}},
    {{w_graph}},
    {{r_member}},
    {{w_member}},
    {{r_setting}},
    {{w_setting}},
    {{hidden}},
    {{lock}},
    '{{created_at}}'
WHERE
    NOT EXISTS (
        SELECT uid
        FROM {TABLE_ROLE}
        WHERE slug='{{slug}}'
    );
"""


def get_safe_insert_role_query(
    slug: str,
    name: Optional[str] = None,
    r_layout=False,
    w_layout=False,
    r_storage=False,
    w_storage=False,
    r_manager=False,
    w_manager=False,
    r_graph=False,
    w_graph=False,
    r_member=False,
    w_member=False,
    r_setting=False,
    w_setting=False,
    hidden=False,
    lock=False,
    created_at: Optional[datetime] = None,
) -> str:
    created = created_at if created_at else today()
    return _INITIALIZE_ONLY_INSERT_ROLE_FORMAT.format(
        slug=slug,
        name=name if name else slug,
        r_layout=r_layout,
        w_layout=w_layout,
        r_storage=r_storage,
        w_storage=w_storage,
        r_manager=r_manager,
        w_manager=w_manager,
        r_graph=r_graph,
        w_graph=w_graph,
        r_member=r_member,
        w_member=w_member,
        r_setting=r_setting,
        w_setting=w_setting,
        hidden=hidden,
        lock=lock,
        created_at=created,
    )


_INSERT_ROLE_OWNER = get_safe_insert_role_query(
    ROLE_SLUG_OWNER,
    r_layout=True,
    w_layout=True,
    r_storage=True,
    w_storage=True,
    r_manager=True,
    w_manager=True,
    r_graph=True,
    w_graph=True,
    r_member=True,
    w_member=True,
    r_setting=True,
    w_setting=True,
    lock=True,
)
_INSERT_ROLE_MAINTAINER = get_safe_insert_role_query(
    ROLE_SLUG_MAINTAINER,
    r_layout=True,
    w_layout=True,
    r_storage=True,
    w_storage=True,
    r_manager=True,
    w_manager=True,
    r_graph=True,
    w_graph=True,
    r_member=True,
    w_member=True,
    r_setting=True,
    w_setting=True,
)
_INSERT_ROLE_DEVELOPER = get_safe_insert_role_query(
    ROLE_SLUG_DEVELOPER,
    r_layout=True,
    w_layout=True,
    r_storage=True,
    w_storage=True,
    r_manager=True,
    w_manager=True,
    r_graph=True,
    w_graph=True,
)
_INSERT_ROLE_REPORTER = get_safe_insert_role_query(
    ROLE_SLUG_REPORTER,
    r_layout=True,
    r_storage=True,
    r_manager=True,
)
_INSERT_ROLE_GUEST = get_safe_insert_role_query(
    ROLE_SLUG_GUEST,
    r_layout=True,
)

INSERT_ROLE_DEFAULTS = (
    _INSERT_ROLE_OWNER,
    _INSERT_ROLE_MAINTAINER,
    _INSERT_ROLE_DEVELOPER,
    _INSERT_ROLE_REPORTER,
    _INSERT_ROLE_GUEST,
)

INSERT_ROLE = f"""
INSERT INTO {TABLE_ROLE} (
    slug,
    name,
    description,
    features,
    extra,
    r_layout,
    w_layout,
    r_storage,
    w_storage,
    r_manager,
    w_manager,
    r_graph,
    w_graph,
    r_member,
    w_member,
    r_setting,
    w_setting,
    hidden,
    lock,
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
    $11, $12, $13, $14, $15, $16, $17, $18, $19, $20
) RETURNING uid;
"""

##########
# UPDATE #
##########


def get_update_role_query_by_uid(
    uid: int,
    slug: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    features: Optional[List[str]] = None,
    extra: Optional[Any] = None,
    r_layout: Optional[bool] = None,
    w_layout: Optional[bool] = None,
    r_storage: Optional[bool] = None,
    w_storage: Optional[bool] = None,
    r_manager: Optional[bool] = None,
    w_manager: Optional[bool] = None,
    r_graph: Optional[bool] = None,
    w_graph: Optional[bool] = None,
    r_member: Optional[bool] = None,
    w_member: Optional[bool] = None,
    r_setting: Optional[bool] = None,
    w_setting: Optional[bool] = None,
    hidden: Optional[bool] = None,
    lock: Optional[bool] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else today()
    builder = UpdateBuilder(
        if_none_skip=True,
        slug=slug,
        name=name,
        description=description,
        features=features,
        extra=extra,
        r_layout=r_layout,
        w_layout=w_layout,
        r_storage=r_storage,
        w_storage=w_storage,
        r_manager=r_manager,
        w_manager=w_manager,
        r_graph=r_graph,
        w_graph=w_graph,
        r_member=r_member,
        w_member=w_member,
        r_setting=r_setting,
        w_setting=w_setting,
        hidden=hidden,
        lock=lock,
        updated_at=updated,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_ROLE)


##########
# DELETE #
##########

DELETE_ROLE_BY_UID = f"""
DELETE FROM {TABLE_ROLE}
WHERE uid=$1;
"""

##########
# SELECT #
##########

SELECT_ROLE_UID_BY_SLUG = f"""
SELECT uid
FROM {TABLE_ROLE}
WHERE slug=$1;
"""

SELECT_ROLE_SLUG_BY_UID = f"""
SELECT slug
FROM {TABLE_ROLE}
WHERE uid=$1;
"""

SELECT_ROLE_BY_UID = f"""
SELECT *
FROM {TABLE_ROLE}
WHERE uid=$1;
"""

SELECT_ROLE_LOCK_BY_UID = f"""
SELECT lock
FROM {TABLE_ROLE}
WHERE uid=$1;
"""

SELECT_ROLE_ALL = f"""
SELECT *
FROM {TABLE_ROLE};
"""

EXISTS_ROLE_BY_UID = f"""
SELECT EXISTS(
    SELECT *
    FROM {TABLE_ROLE}
    WHERE uid=$1
);
"""

SELECT_ROLE_BY_USER_UID_AND_GROUP_UID = f"""
WITH gm AS (
    SELECT role_uid
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1 AND group_uid=$2
)
SELECT perm.*
FROM {TABLE_ROLE} AS perm, gm
WHERE gm.role_uid=perm.uid;
"""

SELECT_ROLE_BY_USER_UID_AND_PROJECT_UID = f"""
WITH pm AS (
    SELECT role_uid
    FROM {TABLE_PROJECT_MEMBER}
    WHERE user_uid=$1 AND project_uid=$2
)
SELECT perm.*
FROM {TABLE_ROLE} AS perm, pm
WHERE pm.role_uid=perm.uid;
"""
