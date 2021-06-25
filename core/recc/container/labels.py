# -*- coding: utf-8 -*-

from typing import Dict, List, Optional

from recc.variables.labels import (
    RECC_CLUSTER_KEY,
    RECC_CLUSTER_VAL_TRUE,
    RECC_CLUSTER_TRUE,
    RECC_CATEGORY_KEY,
    RECC_CATEGORY_VAL_TASK,
    RECC_CATEGORY_TASK,
    RECC_TASK_GROUP_KEY,
    RECC_TASK_PROJECT_KEY,
    RECC_TASK_TASK_KEY,
)


def task_create_labels(
    group_name: Optional[str] = None,
    project_name: Optional[str] = None,
    task_name: Optional[str] = None,
) -> Dict[str, str]:
    result = {
        RECC_CLUSTER_KEY: RECC_CLUSTER_VAL_TRUE,
        RECC_CATEGORY_KEY: RECC_CATEGORY_VAL_TASK,
    }
    if group_name is not None:
        result[RECC_TASK_GROUP_KEY] = group_name
    if project_name is not None:
        result[RECC_TASK_PROJECT_KEY] = project_name
    if task_name is not None:
        result[RECC_TASK_TASK_KEY] = task_name
    return result


def task_find_labels(
    group_name: Optional[str] = None,
    project_name: Optional[str] = None,
    task_name: Optional[str] = None,
) -> List[str]:
    result = [
        RECC_CLUSTER_TRUE,
        RECC_CATEGORY_TASK,
    ]
    if group_name is not None:
        result.append(f"{RECC_TASK_GROUP_KEY}={group_name}")
    if project_name is not None:
        result.append(f"{RECC_TASK_PROJECT_KEY}={project_name}")
    if task_name is not None:
        result.append(f"{RECC_TASK_TASK_KEY}={task_name}")
    return result
