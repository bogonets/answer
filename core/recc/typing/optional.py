# -*- coding: utf-8 -*-

from typing import Any, Type, TypeVar

_T = TypeVar("_T")


def strip_optional(obj: Any, cls: Type[_T]) -> _T:
    if obj is None:
        return cls()
    else:
        return obj
