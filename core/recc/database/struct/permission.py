# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Permission:
    uid: Optional[int] = None
    slug: Optional[str] = None
    created_at: Optional[datetime] = None
