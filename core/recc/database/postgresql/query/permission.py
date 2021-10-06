# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional, List
from re import sub as re_sub
from recc.variables.database import (
    TABLE_USER,
    TABLE_PROJECT,
    TABLE_PERMISSION,
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    PERMISSION_NAME_GUEST,
    PERMISSION_NAME_REPORTER,
    PERMISSION_NAME_OPERATOR,
    PERMISSION_NAME_MAINTAINER,
    PERMISSION_NAME_OWNER,
)
from recc.database.query_builder import UpdateBuilder, BuildResult

##########
# INSERT #
##########

SAFE_INSERT_PERMISSION_GUEST = f"""
INSERT INTO {TABLE_PERMISSION} (
    name,
    r_layout,
    created_at
) SELECT
    '{PERMISSION_NAME_GUEST}',
    True,
    $1
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_PERMISSION}
        WHERE name LIKE '{PERMISSION_NAME_GUEST}'
    );
"""

SAFE_INSERT_PERMISSION_REPORTER = f"""
INSERT INTO {TABLE_PERMISSION} (
    name,
    r_layout,
    r_storage,
    r_manager,
    r_graph,
    created_at
) SELECT
    '{PERMISSION_NAME_REPORTER}',
    True,
    True,
    True,
    True,
    $1
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_PERMISSION}
        WHERE name LIKE '{PERMISSION_NAME_REPORTER}'
    );
"""

SAFE_INSERT_PERMISSION_OPERATOR = f"""
INSERT INTO {TABLE_PERMISSION} (
    name,
    r_layout,
    w_layout,
    r_storage,
    w_storage,
    r_manager,
    w_manager,
    r_graph,
    w_graph,
    created_at
) SELECT
    '{PERMISSION_NAME_OPERATOR}',
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    $1
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_PERMISSION}
        WHERE name LIKE '{PERMISSION_NAME_OPERATOR}'
    );
"""

SAFE_INSERT_PERMISSION_MAINTAINER = f"""
INSERT INTO {TABLE_PERMISSION} (
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
    created_at
) SELECT
    '{PERMISSION_NAME_MAINTAINER}',
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    $1
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_PERMISSION}
        WHERE name LIKE '{PERMISSION_NAME_MAINTAINER}'
    );
"""

SAFE_INSERT_PERMISSION_OWNER = f"""
INSERT INTO {TABLE_PERMISSION} (
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
    created_at
) SELECT
    '{PERMISSION_NAME_OWNER}',
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    $1
WHERE
    NOT EXISTS(
        SELECT uid
        FROM {TABLE_PERMISSION}
        WHERE name LIKE '{PERMISSION_NAME_OWNER}'
    );
"""

SAFE_INSERT_PERMISSION_DEFAULTS = (
    SAFE_INSERT_PERMISSION_GUEST,
    SAFE_INSERT_PERMISSION_REPORTER,
    SAFE_INSERT_PERMISSION_OPERATOR,
    SAFE_INSERT_PERMISSION_MAINTAINER,
    SAFE_INSERT_PERMISSION_OWNER,
)

INSERT_PERMISSION = f"""
INSERT INTO {TABLE_PERMISSION} (
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
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17
) RETURNING uid;
"""

##########
# UPDATE #
##########


def get_update_permission_query_by_uid(
    uid: int,
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
    updated_at=datetime.utcnow().astimezone(),
) -> BuildResult:
    assert updated_at is not None
    builder = UpdateBuilder(
        if_none_skip=True,
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
        updated_at=updated_at,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_PERMISSION)


##########
# DELETE #
##########

DELETE_PERMISSION_BY_UID = f"""
DELETE FROM {TABLE_PERMISSION}
WHERE uid=$1;
"""

SAFE_DELETE_PERMISSION_BY_UID = f"""
BEGIN;

DELETE FROM {TABLE_PROJECT_MEMBER}
WHERE permission_uid=$1;

DELETE FROM {TABLE_GROUP_MEMBER}
WHERE permission_uid=$1;

DELETE FROM {TABLE_PERMISSION}
WHERE uid=$1;

COMMIT;
"""

##########
# SELECT #
##########

SELECT_PERMISSION_GUEST_UID = f"""
SELECT uid
FROM {TABLE_PERMISSION}
WHERE name LIKE '{PERMISSION_NAME_GUEST}';
"""

SELECT_PERMISSION_REPORTER_UID = f"""
SELECT uid
FROM {TABLE_PERMISSION}
WHERE name LIKE '{PERMISSION_NAME_REPORTER}';
"""

SELECT_PERMISSION_OPERATOR_UID = f"""
SELECT uid
FROM {TABLE_PERMISSION}
WHERE name LIKE '{PERMISSION_NAME_OPERATOR}';
"""

SELECT_PERMISSION_MAINTAINER_UID = f"""
SELECT uid
FROM {TABLE_PERMISSION}
WHERE name LIKE '{PERMISSION_NAME_MAINTAINER}';
"""

SELECT_PERMISSION_OWNER_UID = f"""
SELECT uid
FROM {TABLE_PERMISSION}
WHERE name LIKE '{PERMISSION_NAME_OWNER}';
"""

SELECT_PERMISSION_UID_BY_NAME = f"""
SELECT uid
FROM {TABLE_PERMISSION}
WHERE name LIKE $1;
"""

SELECT_PERMISSION_NAME_BY_UID = f"""
SELECT name
FROM {TABLE_PERMISSION}
WHERE uid=$1;
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

##################
# COMPLEX SELECT #
##################

# Best permission of project
# Use the project permission if it exists, and use the group permission if it doesn't.
SELECT_BEST_PERMISSION_OF_PROJECT = f"""
SELECT
    -- u.uid AS user_uid,
    -- p.uid AS project_uid,
    -- p.group_uid AS group_uid,
    -- pm.permission_uid AS pm_permission_uid,
    -- gm.permission_uid AS gm_permission_uid,
    perm.*
FROM
    (SELECT uid FROM {TABLE_USER} WHERE uid=$1) u
    CROSS JOIN (SELECT uid, group_uid FROM {TABLE_PROJECT} WHERE uid=$2) p
    LEFT JOIN {TABLE_GROUP_MEMBER} gm ON gm.user_uid=u.uid AND gm.group_uid=p.group_uid
    LEFT JOIN {TABLE_PROJECT_MEMBER} pm ON pm.user_uid=u.uid AND pm.project_uid=p.uid
    LEFT JOIN {TABLE_PERMISSION} perm ON
        perm.uid=COALESCE(pm.permission_uid, gm.permission_uid)
ORDER BY u.uid, p.uid;
"""

SELECT_BEST_PERMISSION_OF_PROJECT_NO_COMMENT = re_sub(
    r"^  +--.*\n", "", SELECT_BEST_PERMISSION_OF_PROJECT
)

SELECT_PERMISSION_BY_USER_UID_AND_GROUP_UID = f"""
WITH gm AS (
    SELECT permission_uid
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1 AND group_uid=$2
)
SELECT perm.*
FROM {TABLE_PERMISSION} AS perm, gm
WHERE gm.permission_uid=perm.uid;
"""

SELECT_PERMISSION_BY_USER_UID_AND_PROJECT_UID = f"""
WITH pm AS (
    SELECT permission_uid
    FROM {TABLE_PROJECT_MEMBER}
    WHERE user_uid=$1 AND project_uid=$2
)
SELECT perm.*
FROM {TABLE_PERMISSION} AS perm, pm
WHERE pm.permission_uid=perm.uid;
"""
