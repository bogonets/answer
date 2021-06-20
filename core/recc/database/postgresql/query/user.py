# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional
from recc.variables.database import TABLE_USER, VIEW_USER_ADMIN_COUNT
from recc.database.query_builder import UpdateBuilder, BuildResult


##########
# INSERT #
##########

INSERT_USER = f"""
INSERT INTO {TABLE_USER}
    (username, password, salt, email, phone1, phone2, is_admin, extra, created_at)
VALUES
    ($1, $2, $3, $4, $5, $6, $7, $8, $9);
"""

##########
# UPDATE #
##########

UPDATE_USER_LAST_LOGIN_BY_USERNAME = f"""
UPDATE {TABLE_USER}
SET last_login=$2
WHERE username LIKE $1;
"""

UPDATE_USER_USERNAME_BY_UID = f"""
UPDATE {TABLE_USER}
SET username=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_USER_PASSWORD_AND_SALT_BY_UID = f"""
UPDATE {TABLE_USER}
SET password=$2, salt=$3, updated_at=$4
WHERE uid=$1;
"""

UPDATE_USER_PASSWORD_AND_SALT_BY_USERNAME = f"""
UPDATE {TABLE_USER}
SET password=$2, salt=$3, updated_at=$4
WHERE username LIKE $1;
"""

UPDATE_USER_EXTRA_BY_UID = f"""
UPDATE {TABLE_USER}
SET extra=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_USER_EXTRA_BY_USERNAME = f"""
UPDATE {TABLE_USER}
SET extra=$2, updated_at=$3
WHERE username LIKE $1;
"""


def get_update_user_query_by_username(
    username: str,
    email: Optional[str] = None,
    phone1: Optional[str] = None,
    phone2: Optional[str] = None,
    is_admin: Optional[bool] = None,
    extra: Optional[Any] = None,
    updated_at=datetime.utcnow(),
) -> BuildResult:
    assert updated_at is not None
    builder = UpdateBuilder(
        if_none_skip=True,
        email=email,
        phone1=phone1,
        phone2=phone2,
        is_admin=is_admin,
        extra=extra,
        updated_at=updated_at,
    )
    builder.where().eq(username=username)
    return builder.build(TABLE_USER)


##########
# DELETE #
##########

DELETE_USER_BY_UID = f"""
DELETE FROM {TABLE_USER}
WHERE uid=$1;
"""

DELETE_USER_BY_USERNAME = f"""
DELETE FROM {TABLE_USER}
WHERE username LIKE $1;
"""

##########
# SELECT #
##########

SELECT_USER_UID_BY_USERNAME = f"""
SELECT uid
FROM {TABLE_USER}
WHERE username LIKE $1;
"""

SELECT_USER_PASSWORD_AND_SALT_BY_USERNAME = f"""
SELECT password, salt
FROM {TABLE_USER}
WHERE username LIKE $1;
"""

SELECT_USER_EXTRA_BY_USERNAME = f"""
SELECT extra
FROM {TABLE_USER}
WHERE username LIKE $1;
"""

SELECT_USER_BY_USERNAME = f"""
SELECT uid, email, phone1, phone2, is_admin, extra, created_at, updated_at, last_login
FROM {TABLE_USER}
WHERE username LIKE $1;
"""

SELECT_USER_ALL = f"""
SELECT uid, username, email, phone1, phone2,
       is_admin, extra, created_at, updated_at, last_login
FROM {TABLE_USER};
"""

SELECT_USER_ADMIN_COUNT = f"""
SELECT count
FROM {VIEW_USER_ADMIN_COUNT};
"""
