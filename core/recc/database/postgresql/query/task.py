# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Dict, Optional
from recc.variables.database import TABLE_GROUP, TABLE_PROJECT, TABLE_TASK
from recc.database.query_builder import UpdateBuilder, BuildResult


##########
# INSERT #
##########

INSERT_TASK = f"""
INSERT INTO {TABLE_TASK} (
    project_uid, name, description, extra,
    rpc_address,
    auth_algorithm, private_key, public_key,
    maximum_restart_count, numa_memory_nodes, base_image_name, publish_ports,
    created_at
) VALUES (
    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
);
"""

##########
# UPDATE #
##########

UPDATE_TASK_DESCRIPTION_BY_UID = f"""
UPDATE {TABLE_TASK}
SET description=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_TASK_DESCRIPTION_BY_PROJECT_UID_AND_NAME = f"""
UPDATE {TABLE_TASK}
SET description=$3, updated_at=$4
WHERE project_uid=$1 AND name LIKE $2;
"""

UPDATE_TASK_EXTRA_BY_UID = f"""
UPDATE {TABLE_TASK}
SET extra=$2, updated_at=$3
WHERE uid=$1;
"""

UPDATE_TASK_EXTRA_BY_PROJECT_UID_AND_NAME = f"""
UPDATE {TABLE_TASK}
SET extra=$3, updated_at=$4
WHERE project_uid=$1 AND name LIKE $2;
"""

UPDATE_TASK_KEYS_BY_UID = f"""
UPDATE {TABLE_TASK}
SET auth_algorithm=$2, private_key=$3, public_key=$4, updated_at=$5
WHERE uid=$1;
"""

UPDATE_TASK_KEYS_BY_PROJECT_UID_AND_NAME = f"""
UPDATE {TABLE_TASK}
SET auth_algorithm=$3, private_key=$4, public_key=$5, updated_at=$6
WHERE project_uid=$1 AND name LIKE $2;
"""


def get_update_task_query_by_uid(
    uid: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    extra: Optional[Any] = None,
    rpc_address: Optional[str] = None,
    auth_algorithm: Optional[str] = None,
    private_key: Optional[str] = None,
    public_key: Optional[str] = None,
    maximum_restart_count: Optional[int] = None,
    numa_memory_nodes: Optional[str] = None,
    base_image_name: Optional[str] = None,
    publish_ports: Optional[Dict[str, Any]] = None,
    updated_at=datetime.utcnow(),
) -> BuildResult:
    assert updated_at is not None
    builder = UpdateBuilder(
        if_none_skip=True,
        name=name,
        description=description,
        extra=extra,
        rpc_address=rpc_address,
        auth_algorithm=auth_algorithm,
        private_key=private_key,
        public_key=public_key,
        maximum_restart_count=maximum_restart_count,
        numa_memory_nodes=numa_memory_nodes,
        base_image_name=base_image_name,
        publish_ports=publish_ports,
        updated_at=updated_at,
    )
    builder.where().eq(uid=uid)
    return builder.build(TABLE_TASK)


##########
# DELETE #
##########

DELETE_TASK_BY_UID = f"""
DELETE FROM {TABLE_TASK}
WHERE uid=$1;
"""

DELETE_TASK_BY_PROJECT_UID_AND_NAME = f"""
DELETE FROM {TABLE_TASK}
WHERE project_uid=$1 AND name LIKE $2;
"""

##########
# SELECT #
##########

SELECT_TASK_BY_UID = f"""
SELECT *
FROM {TABLE_TASK}
WHERE uid=$1;
"""

SELECT_TASK_BY_PROJECT_ID_AND_NAME = f"""
SELECT *
FROM {TABLE_TASK}
WHERE project_uid=$1 AND name LIKE $2;
"""

SELECT_TASK_UID_BY_PROJECT_ID_AND_NAME = f"""
SELECT uid
FROM {TABLE_TASK}
WHERE project_uid=$1 AND name LIKE $2;
"""

SELECT_TASK_BY_PROJECT_ID = f"""
SELECT *
FROM {TABLE_TASK}
WHERE project_uid=$1;
"""

SELECT_TASK_BY_FULLPATH = f"""
SELECT t.*
FROM (SELECT uid FROM {TABLE_GROUP} WHERE name LIKE $1) g
    LEFT JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid AND p.name LIKE $2
    LEFT JOIN {TABLE_TASK} t ON t.project_uid=p.uid AND t.name LIKE $3;
"""

SELECT_TASK_UID_BY_FULLPATH = f"""
SELECT t.uid AS uid
FROM (SELECT uid FROM {TABLE_GROUP} WHERE name LIKE $1) g
    LEFT JOIN {TABLE_PROJECT} p ON p.group_uid=g.uid AND p.name LIKE $2
    LEFT JOIN {TABLE_TASK} t ON t.project_uid=p.uid AND t.name LIKE $3;
"""
