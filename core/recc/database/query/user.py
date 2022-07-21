# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional

from recc.chrono.datetime import tznow
from recc.database.query_builder import BuildResult, UpdateBuilder
from recc.variables.database import (
    TABLE_GROUP_MEMBER,
    TABLE_PROJECT_MEMBER,
    TABLE_USER,
    VIEW_USER_ADMIN_COUNT,
)

INSERT_USER = f"""
INSERT INTO {TABLE_USER} (
    username,
    password,
    salt,
    nickname,
    email,
    phone,
    admin,
    dark,
    lang,
    timezone,
    created_at,
    updated_at
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
    $10,
    $11,
    $11
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
    phone: Optional[str] = None,
    admin: Optional[bool] = None,
    dark: Optional[int] = None,
    lang: Optional[str] = None,
    timezone: Optional[str] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else tznow()
    builder = UpdateBuilder(
        if_none_skip=True,
        username=username,
        nickname=nickname,
        email=email,
        phone=phone,
        admin=admin,
        dark=dark,
        lang=lang,
        timezone=timezone,
        updated_at=updated,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_USER)
