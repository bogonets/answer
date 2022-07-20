# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_GROUP, TABLE_GROUP_MEMBER, TABLE_PROJECT

INSERT_GROUP_MEMBER = f"""
INSERT INTO {TABLE_GROUP_MEMBER} (
    group_uid,
    user_uid,
    role_uid
) VALUES (
    $1, $2, $3
);
"""

UPDATE_GROUP_MEMBER_ROLE = f"""
UPDATE {TABLE_GROUP_MEMBER}
SET role_uid=$3
WHERE group_uid=$1 AND user_uid=$2;
"""

DELETE_GROUP_MEMBER = f"""
DELETE FROM {TABLE_GROUP_MEMBER}
WHERE group_uid=$1 AND user_uid=$2;
"""

SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID = f"""
SELECT *
FROM {TABLE_GROUP_MEMBER}
WHERE group_uid=$1 AND user_uid=$2;
"""

SELECT_GROUP_MEMBER_BY_GROUP_UID = f"""
SELECT *
FROM {TABLE_GROUP_MEMBER}
WHERE group_uid=$1;
"""

SELECT_GROUP_MEMBER_BY_USER_UID = f"""
SELECT *
FROM {TABLE_GROUP_MEMBER}
WHERE user_uid=$1;
"""

SELECT_GROUP_MEMBER_ALL = f"""
SELECT group_uid, user_uid, role_uid
FROM {TABLE_GROUP_MEMBER};
"""

SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID = f"""
WITH gm AS (
    SELECT *
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1
)
SELECT *
FROM gm
INNER JOIN {TABLE_GROUP} g ON gm.group_uid=g.uid;
"""

SELECT_GROUP_MEMBER_JOIN_GROUP_BY_USER_UID_AND_GROUP_UID = f"""
WITH gm AS (
    SELECT *
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1 AND group_uid=$2
)
SELECT *
FROM gm
INNER JOIN {TABLE_GROUP} g ON gm.group_uid=g.uid;
"""

SELECT_GROUP_MEMBER_JOIN_PROJECT_BY_USER_UID = f"""
WITH gm AS (
    SELECT *
    FROM {TABLE_GROUP_MEMBER}
    WHERE user_uid=$1
)
SELECT *
FROM gm
INNER JOIN {TABLE_PROJECT} p ON gm.group_uid=p.group_uid;
"""
