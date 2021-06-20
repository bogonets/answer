# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Any
from datetime import datetime
from recc.struct._structure import _Structure


class LayoutState(Enum):
    DISABLE = 0
    ENABLE = 1


class Layout(_Structure):
    def __init__(
        self,
        uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        self.uid = uid
        self.project_uid = project_uid
        self.name = name
        self.description = description
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
        self.kwargs = kwargs

    # def is_disable_state(self) -> bool:
    #     if self.state is None:
    #         return True
    #     return self.state == LayoutState.DISABLE
    #
    # def is_enable_state(self) -> bool:
    #     if self.state is None:
    #         return False
    #     return self.state == LayoutState.ENABLE
