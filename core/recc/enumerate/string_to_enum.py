# -*- coding: utf-8 -*-

from typing import TypeVar, Type, Dict
from enum import Enum

_ASSERT_MSG_NOT_ENUM_FORMAT = "The `{cls}` type must inherit from Enum class."
_T = TypeVar("_T")


def string_to_enum(name: str, cls: Type[_T]) -> _T:
    assert issubclass(cls, Enum), _ASSERT_MSG_NOT_ENUM_FORMAT.format(cls=cls.__name__)
    enums = [s for s in dir(cls) if not s.startswith("_")]
    if name in enums:
        return getattr(cls, name)
    raise KeyError(f"Not found `{name}` enum in {cls.__name__}")


def string_to_enum_map(cls: Type[_T]) -> Dict[str, _T]:
    assert issubclass(cls, Enum), _ASSERT_MSG_NOT_ENUM_FORMAT.format(cls=cls.__name__)
    enums = [s for s in dir(cls) if not s.startswith("_")]
    return {e: getattr(cls, e) for e in enums}


def lower_string_to_enum_map(cls: Type[_T]) -> Dict[str, _T]:
    assert issubclass(cls, Enum), _ASSERT_MSG_NOT_ENUM_FORMAT.format(cls=cls.__name__)
    enums = [s for s in dir(cls) if not s.startswith("_")]
    return {e.lower(): getattr(cls, e) for e in enums}
