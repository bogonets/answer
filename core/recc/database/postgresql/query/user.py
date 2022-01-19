# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional
from recc.chrono.datetime import today
from recc.variables.database import (
    TABLE_USER,
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    VIEW_USER_ADMIN_COUNT,
)
from recc.database.query_builder import UpdateBuilder, BuildResult

INSERT_USER = f"""
INSERT INTO {TABLE_USER} (
    username,
    password,
    salt,
    nickname,
    email,
    phone1,
    phone2,
    is_admin,
    extra,
    created_at
) VALUES (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    $7,
    $8,
    $9,
    $10
) RETURNING uid;
"""

UPDATE_USER_LAST_LOGIN_BY_UID = f"""
UPDATE
    {TABLE_USER}
SET
    last_login=$2
WHERE
    uid=$1;
"""

UPDATE_USER_PASSWORD_AND_SALT_BY_UID = f"""
UPDATE
    {TABLE_USER}
SET
    password=$2,
    salt=$3,
    updated_at=$4
WHERE
    uid=$1;
"""

UPDATE_USER_EXTRA_BY_UID = f"""
UPDATE
    {TABLE_USER}
SET
    extra=$2,
    updated_at=$3
WHERE
    uid=$1;
"""

DELETE_USER_BY_UID = f"""
DELETE FROM {TABLE_USER}
WHERE uid=$1;
"""

SAFE_DELETE_USER_BY_UID = f"""
BEGIN;

DELETE FROM {TABLE_PROJECT_MEMBER}
WHERE user_uid=$1;

DELETE FROM {TABLE_GROUP_MEMBER}
WHERE user_uid=$1;

DELETE FROM {TABLE_USER}
WHERE uid=$1;

COMMIT;
"""

SELECT_USER_USERNAME_BY_UID = f"""
SELECT username
FROM {TABLE_USER}
WHERE uid=$1;
"""

SELECT_USER_UID_BY_USERNAME = f"""
SELECT uid
FROM {TABLE_USER}
WHERE username=$1;
"""

SELECT_USER_EXISTS_BY_USERNAME = f"""
SELECT exists(
    SELECT uid
    FROM {TABLE_USER}
    WHERE username=$1
);
"""

SELECT_USER_PASSWORD_AND_SALT_BY_UID = f"""
SELECT password, salt
FROM {TABLE_USER}
WHERE uid=$1;
"""

SELECT_USER_EXTRA_BY_UID = f"""
SELECT extra
FROM {TABLE_USER}
WHERE uid=$1;
"""

SELECT_USER_BY_UID = f"""
SELECT *
FROM {TABLE_USER}
WHERE uid=$1;
"""

SELECT_USER_ALL = f"""
SELECT *
FROM {TABLE_USER};
"""

SELECT_USER_USERNAME = f"""
SELECT username
FROM {TABLE_USER};
"""

SELECT_USER_ADMIN_COUNT = f"""
SELECT count
FROM {VIEW_USER_ADMIN_COUNT};
"""

SELECT_USER_COUNT = f"""
SELECT count(uid) AS count
FROM {TABLE_USER};
"""


def get_update_user_query_by_uid(
    uid: int,
    username: Optional[str] = None,
    nickname: Optional[str] = None,
    email: Optional[str] = None,
    phone1: Optional[str] = None,
    phone2: Optional[str] = None,
    is_admin: Optional[bool] = None,
    extra: Optional[Any] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else today()
    builder = UpdateBuilder(
        if_none_skip=True,
        username=username,
        nickname=nickname,
        email=email,
        phone1=phone1,
        phone2=phone2,
        is_admin=is_admin,
        extra=extra,
        updated_at=updated,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_USER)
