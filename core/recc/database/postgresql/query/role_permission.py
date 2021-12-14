# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_ROLE_PERMISSION

##########
# INSERT #
##########

INSERT_ROLE_PERMISSION = f"""
INSERT INTO {TABLE_ROLE_PERMISSION} (
    role_uid,
    permission_uid
) VALUES (
    $1,
    $2
);
"""

##########
# DELETE #
##########

DELETE_ROLE_PERMISSION = f"""
DELETE FROM {TABLE_ROLE_PERMISSION}
WHERE role_uid=$1 AND permission_uid=$2;
"""

##########
# SELECT #
##########

SELECT_ROLE_PERMISSION_ALL = f"""
SELECT *
FROM {TABLE_ROLE_PERMISSION};
"""
