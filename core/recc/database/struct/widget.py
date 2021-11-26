# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


class WidgetState(Enum):
    DISABLE = 0
    ENABLE = 1


@dataclass
class Widget:
    uid: Optional[int] = None
    layout_uid: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    type_name: Optional[str] = None
    pos_x1: Optional[float] = None
    pos_y1: Optional[float] = None
    pos_x2: Optional[float] = None
    pos_y2: Optional[float] = None
    z_order: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
