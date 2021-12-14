# -*- coding: utf-8 -*-

from recc.variables.database import TABLE_ROLE_PERMISSION

##########
# INSERT #
##########

_INITIALIZE_ONLY_INSERT_ROLE_PERMISSION_FORMAT = f"""
INSERT INTO {TABLE_ROLE_PERMISSION} (
    role_uid,
    permission_uid
) SELECT
    {{role_uid}},
    {{permission_uid}}
WHERE
    NOT EXISTS (
        SELECT *
        FROM {TABLE_ROLE_PERMISSION}
        WHERE role_uid={{role_uid}} AND permission_uid={{permission_uid}}
    );
"""


def get_safe_insert_role_permission_query(role_uid: int, permission_uid: int) -> str:
    return _INITIALIZE_ONLY_INSERT_ROLE_PERMISSION_FORMAT.format(
        role_uid=role_uid,
        permission_uid=permission_uid,
    )


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
