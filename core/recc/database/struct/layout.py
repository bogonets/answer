# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Any, Final
from datetime import datetime
from recc.struct.structure_base import StructureBase
from recc.algorithm.lexicographical import lexicographical_equals


class LayoutState(Enum):
    DISABLE = 0
    ENABLE = 1


class Layout(StructureBase):
    def __init__(
        self,
        uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.uid = uid
        self.project_uid = project_uid
        self.name = name
        self.description = description
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at


class LayoutKeys:
    uid = "uid"
    project_uid = "project_uid"
    name = "name"
    description = "description"
    extra = "extra"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[LayoutKeys] = LayoutKeys()
assert lexicographical_equals(keys, Layout())
