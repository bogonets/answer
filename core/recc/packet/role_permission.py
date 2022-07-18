# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class RolePermission:
    """It is mapped to the `role_permission` table in the database."""

    role_uid: Optional[int] = None
    permission_uid: Optional[int] = None
