# -*- coding: utf-8 -*-

from re import compile as re_compile
from typing import List, Optional, Pattern, Sequence, Union

UnionPattern = Union[str, Pattern]


def compile_pattern(pattern: UnionPattern) -> Pattern:
    if isinstance(pattern, str):
        return re_compile(pattern)
    elif isinstance(pattern, Pattern):
        return pattern
    else:
        raise TypeError(f"Unsupported pattern type: `{type(pattern).__name__}`")


def compile_patterns(
    patterns: Optional[Sequence[UnionPattern]] = None,
) -> List[Pattern]:
    if not patterns:
        return list()
    return [compile_pattern(p) for p in patterns]


def deny(name: str, patterns: List[Pattern]) -> bool:
    for p in patterns:
        if p.match(name) is not None:
            return True
    return False


def allow(name: str, patterns: List[Pattern]) -> bool:
    for p in patterns:
        if p.match(name) is not None:
            return True
    return False


def access_filter(
    names: List[str],
    denies: Optional[Sequence[UnionPattern]] = None,
    allows: Optional[Sequence[UnionPattern]] = None,
) -> List[str]:
    result = list()

    deny_patterns = compile_patterns(denies)
    allow_patterns = compile_patterns(allows)

    for name in names:
        # The `denies` argument list has high priority.
        if deny_patterns:
            if deny(name, deny_patterns):
                continue

        # If the `allows` argument is not defined,
        # Add all modules that are not `denied`.
        if not allow_patterns:
            result.append(name)
            continue

        if allow(name, allow_patterns):
            result.append(name)
            continue

    return result
