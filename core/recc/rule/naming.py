# -*- coding: utf-8 -*-

from re import compile as re_compile
from functools import reduce
from recc.variables.rule_naming import (
    INVALID_NAMING_RULE_PATTERN,
    PREFIX_RECC,
    NAME_SEPARATOR,
    NAME_CONTAINER,
    NAME_VOLUME,
    NAME_NETWORK,
)

_INVALID_NAMING_RULE_REGEX = re_compile(INVALID_NAMING_RULE_PATTERN)


def valid_naming(name: str) -> bool:
    return _INVALID_NAMING_RULE_REGEX.match(name) is None


def naming_merge(*names) -> str:
    return reduce(lambda x, y: f"{x}{NAME_SEPARATOR}{y}", (n for n in names if n))


def naming_task(group_name: str, project_name: str, task_name: str) -> str:
    return naming_merge(
        PREFIX_RECC, NAME_CONTAINER, group_name, project_name, task_name
    )


def naming_task_volume(group_name: str, project_name: str) -> str:
    return naming_merge(PREFIX_RECC, NAME_VOLUME, group_name, project_name)


def naming_task_network(group_name: str, project_name: str) -> str:
    return naming_merge(PREFIX_RECC, NAME_NETWORK, group_name, project_name)
