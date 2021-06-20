# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_PROJECT_MEMBER


##########
# INSERT #
##########

INSERT_PROJECT_MEMBER = f"""
INSERT INTO {TABLE_PROJECT_MEMBER}
    (project_uid, user_uid, permission_uid)
VALUES
    ($1, $2, $3);
"""

##########
# UPDATE #
##########

UPDATE_PROJECT_MEMBER_PERMISSION = f"""
UPDATE {TABLE_PROJECT_MEMBER}
SET permission_uid=$3
WHERE project_uid=$1 AND user_uid=$2;
"""

##########
# DELETE #
##########

DELETE_PROJECT_MEMBER = f"""
DELETE FROM {TABLE_PROJECT_MEMBER}
WHERE project_uid=$1 AND user_uid=$2;
"""

##########
# SELECT #
##########

SELECT_PROJECT_MEMBER_BY_PROJECT_UID_AND_USER_UID = f"""
SELECT permission_uid
FROM {TABLE_PROJECT_MEMBER}
WHERE project_uid=$1 AND user_uid=$2;
"""

SELECT_PROJECT_MEMBER_BY_PROJECT_UID = f"""
SELECT user_uid, permission_uid
FROM {TABLE_PROJECT_MEMBER}
WHERE project_uid=$1;
"""

SELECT_PROJECT_MEMBER_BY_USER_UID = f"""
SELECT project_uid, permission_uid
FROM {TABLE_PROJECT_MEMBER}
WHERE user_uid=$1;
"""

SELECT_PROJECT_MEMBER_ALL = f"""
SELECT project_uid, user_uid, permission_uid
FROM {TABLE_PROJECT_MEMBER};
"""
