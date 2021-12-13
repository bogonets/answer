# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional, List
from re import sub as re_sub
from recc.chrono.datetime import today
from recc.variables.database import (
    TABLE_USER,
    TABLE_PROJECT,
    TABLE_RULE,
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    RULE_SLUG_OWNER,
    RULE_SLUG_MAINTAINER,
    RULE_SLUG_DEVELOPER,
    RULE_SLUG_OPERATOR,
    RULE_SLUG_REPORTER,
    RULE_SLUG_GUEST,
)
from recc.database.query_builder import UpdateBuilder, BuildResult

##########
# INSERT #
##########


INITIALIZE_ONLY_INSERT_RULE_FORMAT = f"""
INSERT INTO {TABLE_RULE} (
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
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_RULE}
        WHERE slug='{{slug}}'
    );
"""


def get_safe_insert_rule_query(
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
    return INITIALIZE_ONLY_INSERT_RULE_FORMAT.format(
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


INSERT_RULE_OWNER = get_safe_insert_rule_query(
    RULE_SLUG_OWNER,
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
INSERT_RULE_MAINTAINER = get_safe_insert_rule_query(
    RULE_SLUG_MAINTAINER,
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
INSERT_RULE_DEVELOPER = get_safe_insert_rule_query(
    RULE_SLUG_DEVELOPER,
    r_layout=True,
    w_layout=True,
    r_storage=True,
    w_storage=True,
    r_manager=True,
    w_manager=True,
    r_graph=True,
    w_graph=True,
)
INSERT_RULE_OPERATOR = get_safe_insert_rule_query(
    RULE_SLUG_OPERATOR,
    r_layout=True,
    w_layout=True,
    r_storage=True,
    w_storage=True,
    r_manager=True,
    w_manager=True,
)
INSERT_RULE_REPORTER = get_safe_insert_rule_query(
    RULE_SLUG_REPORTER,
    r_layout=True,
    r_storage=True,
    r_manager=True,
)
INSERT_RULE_GUEST = get_safe_insert_rule_query(
    RULE_SLUG_GUEST,
    r_layout=True,
)

INSERT_RULE_DEFAULTS = (
    INSERT_RULE_OWNER,
    INSERT_RULE_MAINTAINER,
    INSERT_RULE_DEVELOPER,
    INSERT_RULE_OPERATOR,
    INSERT_RULE_REPORTER,
    INSERT_RULE_GUEST,
)

INSERT_RULE = f"""
INSERT INTO {TABLE_RULE} (
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


def get_update_rule_query_by_uid(
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
    return builder.build(TABLE_RULE)


##########
# DELETE #
##########

DELETE_RULE_BY_UID = f"""
DELETE FROM {TABLE_RULE}
WHERE uid=$1;
"""

##########
# SELECT #
##########

SELECT_RULE_UID_BY_SLUG = f"""
SELECT uid
FROM {TABLE_RULE}
WHERE slug=$1;
"""

SELECT_RULE_SLUG_BY_UID = f"""
SELECT slug
FROM {TABLE_RULE}
WHERE uid=$1;
"""

SELECT_RULE_BY_UID = f"""
SELECT *
FROM {TABLE_RULE}
WHERE uid=$1;
"""

SELECT_RULE_LOCK_BY_UID = f"""
SELECT lock
FROM {TABLE_RULE}
WHERE uid=$1;
"""

SELECT_RULE_ALL = f"""
SELECT *
FROM {TABLE_RULE};
"""

EXISTS_RULE_BY_UID = f"""
SELECT EXISTS(
    SELECT *
    FROM {TABLE_RULE}
    WHERE uid=$1
);
"""

##################
# COMPLEX SELECT #
##################

# Best rule of project
# Use the project rule if it exists, and use the group rule if it doesn't.
SELECT_BEST_RULE_OF_PROJECT = f"""
SELECT
    -- u.uid AS user_uid,
    -- p.uid AS project_uid,
    -- p.group_uid AS group_uid,
    -- pm.rule_uid AS pm_rule_uid,
    -- gm.rule_uid AS gm_rule_uid,
    perm.*
FROM
    (SELECT uid FROM {TABLE_USER} WHERE uid=$1) u
    CROSS JOIN (SELECT uid, group_uid FROM {TABLE_PROJECT} WHERE uid=$2) p
    LEFT JOIN {TABLE_GROUP_MEMBER} gm ON gm.user_uid=u.uid AND gm.group_uid=p.group_uid
    LEFT JOIN {TABLE_PROJECT_MEMBER} pm ON pm.user_uid=u.uid AND pm.project_uid=p.uid
    LEFT JOIN {TABLE_RULE} perm ON
        perm.uid=COALESCE(pm.rule_uid, gm.rule_uid)
ORDER BY u.uid, p.uid;
"""

SELECT_BEST_RULE_OF_PROJECT_NO_COMMENT = re_sub(
    r"^  +--.*\n", "", SELECT_BEST_RULE_OF_PROJECT
)

SELECT_RULE_BY_USER_UID_AND_GROUP_UID = f"""
WITH gm AS (
    SELECT rule_uid
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1 AND group_uid=$2
)
SELECT perm.*
FROM {TABLE_RULE} AS perm, gm
WHERE gm.rule_uid=perm.uid;
"""

SELECT_RULE_BY_USER_UID_AND_PROJECT_UID = f"""
WITH pm AS (
    SELECT rule_uid
    FROM {TABLE_PROJECT_MEMBER}
    WHERE user_uid=$1 AND project_uid=$2
)
SELECT perm.*
FROM {TABLE_RULE} AS perm, pm
WHERE pm.rule_uid=perm.uid;
"""
