# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional
from recc.chrono.datetime import today
from recc.variables.database import TABLE_DAEMON
from recc.database.query_builder import UpdateBuilder, BuildResult

INSERT_DAEMON = f"""
INSERT INTO {TABLE_DAEMON} (
    plugin,
    slug,
    name,
    address,
    requirements_sha256,
    description,
    extra,
    enable,
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9
) RETURNING uid;
"""

UPDATE_DAEMON_REQUIREMENTS_SHA256_BY_UID = f"""
UPDATE {TABLE_DAEMON}
SET requirements_sha256=$2, updated_at=$3
WHERE uid=$1;
"""

DELETE_DAEMON_BY_UID = f"""
DELETE FROM {TABLE_DAEMON}
WHERE uid=$1;
"""

DELETE_DAEMON_BY_SLUG = f"""
DELETE FROM {TABLE_DAEMON}
WHERE slug=$1;
"""

SELECT_DAEMON_BY_UID = f"""
SELECT *
FROM {TABLE_DAEMON}
WHERE uid=$1;
"""

SELECT_DAEMON_UID_BY_SLUG = f"""
SELECT uid
FROM {TABLE_DAEMON}
WHERE slug=$1;
"""

SELECT_DAEMON_ADDRESS_BY_SLUG = f"""
SELECT address
FROM {TABLE_DAEMON}
WHERE slug=$1;
"""

SELECT_DAEMON_BY_SLUG = f"""
SELECT *
FROM {TABLE_DAEMON}
WHERE slug=$1;
"""

SELECT_DAEMON_ALL = f"""
SELECT *
FROM {TABLE_DAEMON};
"""


def get_update_daemon_query_by_uid(
    uid: int,
    plugin: Optional[str] = None,
    slug: Optional[str] = None,
    name: Optional[str] = None,
    address: Optional[str] = None,
    requirements_sha256: Optional[str] = None,
    description: Optional[str] = None,
    extra: Optional[Any] = None,
    enable: Optional[bool] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else today()
    builder = UpdateBuilder(
        if_none_skip=True,
        plugin=plugin,
        slug=slug,
        name=name,
        address=address,
        requirements_sha256=requirements_sha256,
        description=description,
        extra=extra,
        enable=enable,
        updated_at=updated,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_DAEMON)
