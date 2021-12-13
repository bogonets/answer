# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_PROJECT, TABLE_PROJECT_MEMBER


##########
# INSERT #
##########

INSERT_PROJECT_MEMBER = f"""
INSERT INTO {TABLE_PROJECT_MEMBER} (
    project_uid,
    user_uid,
    rule_uid
) VALUES (
    $1, $2, $3
);
"""

##########
# UPDATE #
##########

UPDATE_PROJECT_MEMBER_RULE = f"""
UPDATE {TABLE_PROJECT_MEMBER}
SET rule_uid=$3
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
SELECT rule_uid
FROM {TABLE_PROJECT_MEMBER}
WHERE project_uid=$1 AND user_uid=$2;
"""

SELECT_PROJECT_MEMBER_BY_PROJECT_UID = f"""
SELECT user_uid, rule_uid
FROM {TABLE_PROJECT_MEMBER}
WHERE project_uid=$1;
"""

SELECT_PROJECT_MEMBER_BY_USER_UID = f"""
SELECT project_uid, rule_uid
FROM {TABLE_PROJECT_MEMBER}
WHERE user_uid=$1;
"""

SELECT_PROJECT_MEMBER_ALL = f"""
SELECT project_uid, user_uid, rule_uid
FROM {TABLE_PROJECT_MEMBER};
"""

SELECT_PROJECT_MEMBER_JOIN_PROJECT_BY_USER_UID = f"""
WITH pm AS (
    SELECT *
    FROM {TABLE_PROJECT_MEMBER}
    WHERE user_uid=$1
)
SELECT *
FROM pm
INNER JOIN {TABLE_PROJECT} p ON pm.project_uid=p.uid;
"""

SELECT_PROJECT_MEMBER_JOIN_PROJECT_BY_USER_UID_PROJECT_UID = f"""
WITH pm AS (
    SELECT *
    FROM {TABLE_PROJECT_MEMBER}
    WHERE user_uid=$1 AND project_uid=$2
)
SELECT *
FROM pm
INNER JOIN {TABLE_PROJECT} p ON pm.project_uid=p.uid;
"""
