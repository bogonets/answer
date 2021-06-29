# -*- coding: utf-8 -*-

from inspect import getmembers, isroutine
from typing import Any, List, Tuple, Mapping, Iterable


def is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def is_private_member(name: str) -> bool:
    return name.startswith("_")


def is_public_member(name: str) -> bool:
    return not is_private_member(name)


def get_public_members(data: Any) -> List[Tuple[str, Any]]:
    if isinstance(data, Mapping):
        return [(str(k), v) for k, v in data.items()]
    if isinstance(data, Iterable):
        return [(str(i), v) for i, v in enumerate(data)]
    members = getmembers(data, lambda a: not isroutine(a))
    return list(filter(lambda x: is_public_member(x[0]), members))
