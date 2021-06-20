# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_GROUP_MEMBER

##########
# INSERT #
##########

INSERT_GROUP_MEMBER = f"""
INSERT INTO {TABLE_GROUP_MEMBER}
    (group_uid, user_uid, permission_uid)
VALUES
    ($1, $2, $3);
"""

##########
# UPDATE #
##########

UPDATE_GROUP_MEMBER_PERMISSION = f"""
UPDATE {TABLE_GROUP_MEMBER}
SET permission_uid=$3
WHERE group_uid=$1 AND user_uid=$2;
"""

##########
# DELETE #
##########

DELETE_GROUP_MEMBER = f"""
DELETE FROM {TABLE_GROUP_MEMBER}
WHERE group_uid=$1 AND user_uid=$2;
"""

##########
# SELECT #
##########

SELECT_GROUP_MEMBER_BY_GROUP_UID_AND_USER_UID = f"""
SELECT permission_uid
FROM {TABLE_GROUP_MEMBER}
WHERE group_uid=$1 AND user_uid=$2;
"""

SELECT_GROUP_MEMBER_BY_GROUP_UID = f"""
SELECT user_uid, permission_uid
FROM {TABLE_GROUP_MEMBER}
WHERE group_uid=$1;
"""

SELECT_GROUP_MEMBER_BY_USER_UID = f"""
SELECT group_uid, permission_uid
FROM {TABLE_GROUP_MEMBER}
WHERE user_uid=$1;
"""

SELECT_GROUP_MEMBER_ALL = f"""
SELECT group_uid, user_uid, permission_uid
FROM {TABLE_GROUP_MEMBER};
"""
