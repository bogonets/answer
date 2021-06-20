# -*- coding: utf-8 -*-

from typing import Dict, List, Optional

from recc.variables.labels import (
    ANSWER_CLUSTER_KEY,
    ANSWER_CLUSTER_VAL_TRUE,
    ANSWER_CLUSTER_TRUE,
    ANSWER_CLUSTER_CATEGORY_KEY,
    ANSWER_CLUSTER_CATEGORY_VAL_NODE,
    ANSWER_CLUSTER_CATEGORY_NODE,
    ANSWER_CLUSTER_NODE_GROUP_KEY,
    ANSWER_CLUSTER_NODE_PROJECT_KEY,
    ANSWER_CLUSTER_NODE_TASK_KEY,
)


def task_create_labels(
    group_name: Optional[str] = None,
    project_name: Optional[str] = None,
    task_name: Optional[str] = None,
) -> Dict[str, str]:
    result = {
        ANSWER_CLUSTER_KEY: ANSWER_CLUSTER_VAL_TRUE,
        ANSWER_CLUSTER_CATEGORY_KEY: ANSWER_CLUSTER_CATEGORY_VAL_NODE,
    }
    if group_name is not None:
        result[ANSWER_CLUSTER_NODE_GROUP_KEY] = group_name
    if project_name is not None:
        result[ANSWER_CLUSTER_NODE_PROJECT_KEY] = project_name
    if task_name is not None:
        result[ANSWER_CLUSTER_NODE_TASK_KEY] = task_name
    return result


def task_find_labels(
    group_name: Optional[str] = None,
    project_name: Optional[str] = None,
    task_name: Optional[str] = None,
) -> List[str]:
    result = [
        ANSWER_CLUSTER_TRUE,
        ANSWER_CLUSTER_CATEGORY_NODE,
    ]
    if group_name is not None:
        result.append(f"{ANSWER_CLUSTER_NODE_GROUP_KEY}={group_name}")
    if project_name is not None:
        result.append(f"{ANSWER_CLUSTER_NODE_PROJECT_KEY}={project_name}")
    if task_name is not None:
        result.append(f"{ANSWER_CLUSTER_NODE_TASK_KEY}={task_name}")
    return result
