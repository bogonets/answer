# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional
from recc.variables.database import TABLE_PORT
from recc.database.query_builder import UpdateBuilder, BuildResult

##########
# INSERT #
##########

INSERT_PORT = f"""
INSERT INTO {TABLE_PORT} (
    number,
    group_uid,
    project_uid,
    task_uid,
    description,
    extra,
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7
);
"""

##########
# UPDATE #
##########

UPDATE_PORT_DESCRIPTION_BY_NUMBER = f"""
UPDATE {TABLE_PORT}
SET description=$2, updated_at=$3
WHERE number=$1;
"""

UPDATE_PORT_EXTRA_BY_NUMBER = f"""
UPDATE {TABLE_PORT}
SET extra=$2, updated_at=$3
WHERE number=$1;
"""


def get_update_port_query_by_number(
    number: int,
    group_uid: Optional[int] = None,
    project_uid: Optional[int] = None,
    task_uid: Optional[int] = None,
    description: Optional[str] = None,
    extra: Optional[Any] = None,
    updated_at=datetime.utcnow(),
) -> BuildResult:
    assert updated_at is not None
    builder = UpdateBuilder(
        if_none_skip=True,
        group_uid=group_uid,
        project_uid=project_uid,
        task_uid=task_uid,
        description=description,
        extra=extra,
        updated_at=updated_at,
    )
    builder.where().eq(number=number)
    return builder.build(TABLE_PORT)


##########
# DELETE #
##########

DELETE_PORT_BY_NUMBER = f"""
DELETE FROM {TABLE_PORT}
WHERE number=$1;
"""

##########
# SELECT #
##########

SELECT_PORT_BY_NUMBER = f"""
SELECT
    group_uid, project_uid, task_uid,
    description, extra, created_at, updated_at
FROM {TABLE_PORT}
WHERE number=$1;
"""

SELECT_PORT_BY_GROUP_UID = f"""
SELECT
    number, project_uid, task_uid,
    description, extra, created_at, updated_at
FROM {TABLE_PORT}
WHERE group_uid=$1;
"""

SELECT_PORT_BY_PROJECT_UID = f"""
SELECT
    number, group_uid, task_uid,
    description, extra, created_at, updated_at
FROM {TABLE_PORT}
WHERE project_uid=$1;
"""

SELECT_PORT_BY_TASK_UID = f"""
SELECT
    number, group_uid, project_uid,
    description, extra, created_at, updated_at
FROM {TABLE_PORT}
WHERE task_uid=$1;
"""

SELECT_PORT_ALL = f"""
SELECT
    number, group_uid, project_uid, task_uid,
    description, extra, created_at, updated_at
FROM {TABLE_PORT};
"""
