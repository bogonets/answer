# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from recc.chrono.datetime import tznow
from recc.variables.database import TABLE_PORT
from recc.database.query_builder import UpdateBuilder, BuildResult

INSERT_PORT = f"""
INSERT INTO {TABLE_PORT} (
    number,
    sock,
    ref_uid,
    ref_category,
    created_at,
    updated_at
) VALUES (
    $1, $2, $3, $4, $5, $5
);
"""

DELETE_PORT_BY_NUMBER_AND_SOCK = f"""
DELETE FROM {TABLE_PORT}
WHERE number=$1 AND sock=$2;
"""

SELECT_PORT_BY_NUMBER = f"""
SELECT *
FROM {TABLE_PORT}
WHERE number=$1 AND sock=$2;
"""

SELECT_PORT_ALL = f"""
SELECT *
FROM {TABLE_PORT};
"""


def get_update_port_query_by_number(
    number: int,
    sock: int,
    ref_uid: Optional[int] = None,
    ref_category: Optional[str] = None,
    updated_at: Optional[datetime] = None,
) -> BuildResult:
    updated = updated_at if updated_at else tznow()
    builder = UpdateBuilder(
        if_none_skip=True,
        ref_uid=ref_uid,
        ref_category=ref_category,
        updated_at=updated,
    )
    builder.where().eq(number=number).a.eq(sock=sock)
    return builder.build(TABLE_PORT)
