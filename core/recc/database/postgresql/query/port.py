# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional
from recc.chrono.datetime import today
from recc.variables.database import TABLE_PORT
from recc.database.query_builder import UpdateBuilder, BuildResult

INSERT_PORT = f"""
INSERT INTO {TABLE_PORT} (
    number,
    ref_uid,
    ref_category,
    description,
    extra,
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6
);
"""

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

DELETE_PORT_BY_NUMBER = f"""
DELETE FROM {TABLE_PORT}
WHERE number=$1;
"""

SELECT_PORT_BY_NUMBER = f"""
SELECT *
FROM {TABLE_PORT}
WHERE number=$1;
"""

SELECT_PORT_ALL = f"""
SELECT *
FROM {TABLE_PORT};
"""


def get_update_port_query_by_number(
    number: int,
    ref_uid: Optional[int] = None,
    ref_category: Optional[str] = None,
    description: Optional[str] = None,
    extra: Optional[Any] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else today()
    builder = UpdateBuilder(
        if_none_skip=True,
        ref_uid=ref_uid,
        ref_category=ref_category,
        description=description,
        extra=extra,
        updated_at=updated,
    )
    builder.where().eq(number=number)
    return builder.build(TABLE_PORT)
