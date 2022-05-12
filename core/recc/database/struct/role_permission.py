# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class RolePermission:
    role_uid: Optional[int] = None
    permission_uid: Optional[int] = None
