# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass


@dataclass
class UnionMember:
    domain_uid: Optional[int] = None
    user_uid: Optional[int] = None
    role_uid: Optional[int] = None
    category: Optional[int] = None
