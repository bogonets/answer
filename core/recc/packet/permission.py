# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Permission:
    """It is mapped to the `permission` table in the database."""

    uid: Optional[int] = None
    slug: Optional[str] = None
    created_at: Optional[datetime] = None
