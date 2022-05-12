# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class Group:
    uid: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
