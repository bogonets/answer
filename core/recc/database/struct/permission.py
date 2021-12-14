# -*- coding: utf-8 -*-

from typing import Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Permission:
    uid: Optional[int] = None
    slug: Optional[str] = None

    description: Optional[str] = None
    extra: Optional[Any] = None

    created_at: Optional[datetime] = None
