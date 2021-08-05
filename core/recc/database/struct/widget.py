# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Any, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


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

    def remove_sensitive(self):
        self.uid = None
        self.layout_uid = None


class WidgetKeys:
    uid = "uid"
    layout_uid = "layout_uid"
    name = "name"
    description = "description"
    extra = "extra"
    type_name = "type_name"
    pos_x1 = "pos_x1"
    pos_y1 = "pos_y1"
    pos_x2 = "pos_x2"
    pos_y2 = "pos_y2"
    z_order = "z_order"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[WidgetKeys] = WidgetKeys()
assert lexicographical_members(keys, Widget())
