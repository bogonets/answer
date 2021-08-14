# -*- coding: utf-8 -*-

from typing import Tuple
from recc.rule.naming_base import merge_naming, split_naming
from recc.variables.naming import (
    PREFIX_RECC,
    NAME_DELIMITER,
    NAME_CONTAINER,
    NAME_VOLUME,
    NAME_NETWORK,
)


def naming_task(group: str, project: str, task: str) -> str:
    return merge_naming(
        PREFIX_RECC,
        NAME_CONTAINER,
        group,
        project,
        task,
        delimiter=NAME_DELIMITER,
    )


def naming_task_volume(group: str, project: str) -> str:
    return merge_naming(
        PREFIX_RECC,
        NAME_VOLUME,
        group,
        project,
        delimiter=NAME_DELIMITER,
    )


def naming_task_network(group: str, project: str) -> str:
    return merge_naming(
        PREFIX_RECC,
        NAME_NETWORK,
        group,
        project,
        delimiter=NAME_DELIMITER,
    )


def split_task_name(fullname: str) -> Tuple[str, str, str]:
    names = split_naming(fullname, delimiter=NAME_DELIMITER)
    assert len(names) == 5, "The task-name requires 5 fields."
    assert names[0] == PREFIX_RECC, f"The first field must be {PREFIX_RECC}."
    assert names[1] == NAME_CONTAINER, f"The second field must be {NAME_CONTAINER}."
    return names[2], names[3], names[4]
