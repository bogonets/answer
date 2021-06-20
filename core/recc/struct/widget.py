# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Any
from datetime import datetime
from recc.struct._structure import _Structure


class WidgetState(Enum):
    DISABLE = 0
    ENABLE = 1


class Widget(_Structure):
    def __init__(
        self,
        uid: Optional[int] = None,
        layout_uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        type_name: Optional[str] = None,
        pos_x1: Optional[float] = None,
        pos_y1: Optional[float] = None,
        pos_x2: Optional[float] = None,
        pos_y2: Optional[float] = None,
        z_order: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        self.uid = uid
        self.layout_uid = layout_uid
        self.name = name
        self.description = description
        self.extra = extra
        self.type_name = type_name
        self.pos_x1 = pos_x1
        self.pos_y1 = pos_y1
        self.pos_x2 = pos_x2
        self.pos_y2 = pos_y2
        self.z_order = z_order
        self.created_at = created_at
        self.updated_at = updated_at
        self.kwargs = kwargs

    # def is_disable_state(self) -> bool:
    #     if self.state is None:
    #         return True
    #     return self.state == WidgetState.DISABLE
    #
    # def is_enable_state(self) -> bool:
    #     if self.state is None:
    #         return False
    #     return self.state == WidgetState.ENABLE
