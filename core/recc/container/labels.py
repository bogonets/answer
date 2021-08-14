# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Iterable
from recc.variables.labels import (
    RECC_CLUSTER_KEY,
    RECC_CLUSTER_VAL_TRUE,
    RECC_CLUSTER_TRUE,
    RECC_CATEGORY_KEY,
    RECC_CATEGORY_VAL_TASK,
    RECC_CATEGORY_TASK,
    RECC_CATEGORY_IMAGE,
    RECC_TASK_GROUP_KEY,
    RECC_TASK_PROJECT_KEY,
    RECC_TASK_TASK_KEY,
)


def task_create_labels(
    group: Optional[str] = None,
    project: Optional[str] = None,
    task: Optional[str] = None,
) -> Dict[str, str]:
    result = {
        RECC_CLUSTER_KEY: RECC_CLUSTER_VAL_TRUE,
        RECC_CATEGORY_KEY: RECC_CATEGORY_VAL_TASK,
    }
    if group is not None:
        result[RECC_TASK_GROUP_KEY] = group
    if project is not None:
        result[RECC_TASK_PROJECT_KEY] = project
    if task is not None:
        result[RECC_TASK_TASK_KEY] = task
    return result


def task_find_labels(
    group: Optional[str] = None,
    project: Optional[str] = None,
    task: Optional[str] = None,
) -> List[str]:
    result = [
        RECC_CLUSTER_TRUE,
        RECC_CATEGORY_TASK,
    ]
    if group is not None:
        result.append(f"{RECC_TASK_GROUP_KEY}={group}")
    if project is not None:
        result.append(f"{RECC_TASK_PROJECT_KEY}={project}")
    if task is not None:
        result.append(f"{RECC_TASK_TASK_KEY}={task}")
    return result


def task_image_find_labels() -> List[str]:
    return [RECC_CATEGORY_IMAGE]


def find_label(labels: Iterable[str], key: str) -> str:
    for label in labels:
        if label.strip().startswith(key):
            return label
    raise RuntimeError(f"Not found label: {key}")


def find_label_value(labels: Iterable[str], key: str) -> str:
    label = find_label(labels, key)
    key_val = label.split("=", 1)
    assert key == key_val[0].strip()

    if len(key_val) == 1:
        return str()

    assert len(key_val) == 2
    return key_val[1].strip()
