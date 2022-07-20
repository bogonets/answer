# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional

from recc.chrono.datetime import tznow
from recc.database.query_builder import BuildResult, UpdateBuilder
from recc.variables.database import FUNC_ADD_DAEMON_AND_PORT, TABLE_DAEMON

INSERT_DAEMON = f"""
INSERT INTO {TABLE_DAEMON} (
    plugin,
    slug,
    name,
    address,
    description,
    enable,
    created_at,
    updated_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $7
) RETURNING uid;
"""

INSERT_DAEMON_AND_PORT = f"""
SELECT {FUNC_ADD_DAEMON_AND_PORT}()
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
    description: Optional[str] = None,
    enable: Optional[bool] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else tznow()
    builder = UpdateBuilder(
        if_none_skip=True,
        plugin=plugin,
        slug=slug,
        name=name,
        address=address,
        description=description,
        enable=enable,
        updated_at=updated,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_DAEMON)
