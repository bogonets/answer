# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique
from typing import Any, Optional


@unique
class WidgetState(Enum):
    DISABLE = 0
    ENABLE = 1


@dataclass
class Widget:
    """It is mapped to the `widget` table in the database."""

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
