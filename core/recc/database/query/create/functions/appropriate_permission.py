# -*- coding: utf-8 -*-

from recc.variables.database import (
    FUNC_APPROPRIATE_PERMISSION,
    TABLE_GROUP_MEMBER,
    TABLE_PERMISSION,
    TABLE_PROJECT_MEMBER,
    TABLE_ROLE_PERMISSION,
    TABLE_USER,
)

CREATE_FUNC_APPROPRIATE_PERMISSION = f"""
CREATE OR REPLACE FUNCTION {FUNC_APPROPRIATE_PERMISSION} (
    u_uid INTEGER,
    g_uid INTEGER,
    p_uid INTEGER DEFAULT NULL
)
    RETURNS SETOF {TABLE_PERMISSION}
    LANGUAGE plpgsql
AS $function$
DECLARE
    r_uid INTEGER := NULL;
    is_admin BOOLEAN := FALSE;
BEGIN
    SELECT u.admin
    INTO is_admin
    FROM {TABLE_USER} u
    WHERE u.uid=u_uid;

    IF is_admin THEN
        -- Administrator has full control.
        RETURN QUERY
        SELECT *
        FROM {TABLE_PERMISSION};
        RETURN;
    END IF;

    IF NOT p_uid ISNULL THEN
        -- First make sure you are a member of the project.
        SELECT role_uid
        INTO r_uid
        FROM {TABLE_PROJECT_MEMBER}
        WHERE user_uid=u_uid AND project_uid=p_uid;
    END IF;

    IF r_uid ISNULL THEN
        -- If you are not a project member, check the group member.
        SELECT role_uid
        INTO r_uid
        FROM {TABLE_GROUP_MEMBER}
        WHERE user_uid=u_uid AND group_uid=g_uid;
    END IF;

    RETURN QUERY
    SELECT *
    FROM {TABLE_PERMISSION}
    WHERE uid IN (
        SELECT permission_uid
        FROM {TABLE_ROLE_PERMISSION}
        WHERE role_uid=r_uid
    );
END;
$function$;
"""

DROP_FUNC_APPROPRIATE_PERMISSION = f"""
DROP FUNCTION IF EXISTS {FUNC_APPROPRIATE_PERMISSION};
"""

_SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_FORMAT = f"""
SELECT * FROM {FUNC_APPROPRIATE_PERMISSION}({{u_uid}}, {{g_uid}});
"""

_SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_AND_PROJECT_FORMAT = f"""
SELECT * FROM {FUNC_APPROPRIATE_PERMISSION}({{u_uid}}, {{g_uid}}, {{p_uid}});
"""


def get_select_appropriate_permission_by_user_and_group(
    user_uid: int, group_uid: int
) -> str:
    return _SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_FORMAT.format(
        u_uid=user_uid,
        g_uid=group_uid,
    )


def get_select_appropriate_permission_by_user_and_group_and_project(
    user_uid: int, group_uid: int, project_uid: int
) -> str:
    return _SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_AND_PROJECT_FORMAT.format(
        u_uid=user_uid,
        g_uid=group_uid,
        p_uid=project_uid,
    )
