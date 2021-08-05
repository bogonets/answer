# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Any, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


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

    def remove_sensitive(self):
        self.uid = None
        self.project_uid = None


class LayoutKeys:
    uid = "uid"
    project_uid = "project_uid"
    name = "name"
    description = "description"
    extra = "extra"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[LayoutKeys] = LayoutKeys()
assert lexicographical_members(keys, Layout())
