# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class GroupMember:
    """It is mapped to the `group_member` table in the database."""

    group_uid: Optional[int] = None
    user_uid: Optional[int] = None
    role_uid: Optional[int] = None
