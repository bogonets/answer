# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass


@dataclass
class RolePermission:
    role_uid: Optional[int] = None
    permission_uid: Optional[int] = None
