# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
from re import Pattern
from typing import Any, Callable, Iterable, Optional

from recc.regex.access_filter import compile_pattern


@dataclass
class MatchItem:

    file: str
    pattern: Optional[Pattern] = None

    @classmethod
    def parse(cls, o: Any):
        if isinstance(o, str):
            return cls(o)
        elif isinstance(o, (tuple, list)):
            if len(o) == 1:
                assert isinstance(o[0], str)
                return cls(o[0])
            elif len(o) == 2:
                assert isinstance(o[0], str)
                assert isinstance(o[1], str)
                return cls(o[1], compile_pattern(o[0]))
        else:
            raise TypeError(f"Unsupported type: {type(o).__name__}")

    def match(self, test_value: str, cb: Callable[[str], bool]) -> Optional[str]:
        if self.pattern is not None:
            groups = self.pattern.match(test_value)
            if groups is not None:
                substituted_value = self.pattern.sub(self.file, test_value)
                if cb(substituted_value):
                    return substituted_value
        else:
            if cb(self.file):
                return self.file
        return None


def find_match_item(
    matches: Iterable[MatchItem], test_value: str, cb: Callable[[str], bool]
) -> str:
    for m in matches:
        result = m.match(test_value, cb)
        if result is not None:
            return result
    raise IndexError("No matches found")


def find_match_file(
    matches: Iterable[MatchItem], test_value: str, base_dir: str
) -> str:
    def _isfile(x: str) -> bool:
        return os.path.isfile(os.path.join(base_dir, x))

    return find_match_item(matches, test_value, _isfile)
