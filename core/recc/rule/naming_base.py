# -*- coding: utf-8 -*-

from re import compile as re_compile
from typing import List
from functools import reduce
from recc.variables.naming import INVALID_NAMING_RULE_PATTERN

_INVALID_NAMING_RULE_REGEX = re_compile(INVALID_NAMING_RULE_PATTERN)


def valid_naming(name: str) -> bool:
    return _INVALID_NAMING_RULE_REGEX.match(name) is None


def merge_naming(*names, delimiter: str) -> str:
    return reduce(lambda x, y: f"{x}{delimiter}{y}", (n for n in names if n))


def split_naming(fullname: str, delimiter: str) -> List[str]:
    return fullname.split(delimiter)
