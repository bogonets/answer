# -*- coding: utf-8 -*-

from typing import Any
from recc.inspect.member import get_public_members


def lexicographical_equals(left: Any, right: Any) -> bool:
    left_members = [m[0] for m in get_public_members(left)]
    right_members = [m[0] for m in get_public_members(right)]
    if len(left_members) != len(right_members):
        return False
    for m in left_members:
        if m not in right_members:
            return False
    return True
