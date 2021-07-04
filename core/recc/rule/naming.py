# -*- coding: utf-8 -*-

from re import compile as re_compile
from typing import List, Tuple
from functools import reduce
from recc.variables.naming import (
    INVALID_NAMING_RULE_PATTERN,
    PREFIX_RECC,
    NAME_SEPARATOR,
    NAME_CONTAINER,
    NAME_VOLUME,
    NAME_NETWORK,
    SUFFIX_SOCKET,
)

_INVALID_NAMING_RULE_REGEX = re_compile(INVALID_NAMING_RULE_PATTERN)


def valid_naming(name: str) -> bool:
    return _INVALID_NAMING_RULE_REGEX.match(name) is None


def naming_merge(*names) -> str:
    return reduce(lambda x, y: f"{x}{NAME_SEPARATOR}{y}", (n for n in names if n))


def naming_split(name: str) -> List[str]:
    return name.split(NAME_SEPARATOR)


def naming_task(group_name: str, project_name: str, task_name: str) -> str:
    return naming_merge(
        PREFIX_RECC, NAME_CONTAINER, group_name, project_name, task_name
    )


def split_task_name(name: str) -> Tuple[str, str, str]:
    names = naming_split(name)
    assert len(names) == 5
    assert names[0] == PREFIX_RECC
    assert names[1] == NAME_CONTAINER
    return names[2], names[3], names[4]


def naming_task_volume(group_name: str, project_name: str) -> str:
    return naming_merge(PREFIX_RECC, NAME_VOLUME, group_name, project_name)


def naming_task_network(group_name: str, project_name: str) -> str:
    return naming_merge(PREFIX_RECC, NAME_NETWORK, group_name, project_name)


def naming_socket(task_name: str, hidden=False) -> str:
    result = naming_merge(PREFIX_RECC, task_name, SUFFIX_SOCKET)
    if hidden:
        return "." + result
    else:
        return result
