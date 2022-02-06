# -*- coding: utf-8 -*-

from typing import Any
from recc.inspect.member import get_public_attributes


def lexicographical_members(left: Any, right: Any) -> bool:
    left_members = set(m[0] for m in get_public_attributes(left))
    right_members = set(m[0] for m in get_public_attributes(right))
    if len(left_members) != len(right_members):
        return False
    for m in left_members:
        if m not in right_members:
            return False
    return True
