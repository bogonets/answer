# -*- coding: utf-8 -*-

from typing import Any


def any_none(*args: Any) -> bool:
    for arg in args:
        if arg is None:
            return True
    return False


def any_not_none(*args: Any) -> bool:
    for arg in args:
        if arg is not None:
            return True
    return False


def all_none(*args: Any) -> bool:
    for arg in args:
        if arg is not None:
            return False
    return True


def all_not_none(*args: Any) -> bool:
    for arg in args:
        if arg is None:
            return False
    return True
