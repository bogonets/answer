# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class LayoutState(Enum):
    DISABLE = 0
    ENABLE = 1


@dataclass
class Layout:
    uid: Optional[int] = None
    project_uid: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
