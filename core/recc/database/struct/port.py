# -*- coding: utf-8 -*-

from typing import Optional, Any, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


@dataclass
class Port:
    number: Optional[int] = None
    group_uid: Optional[int] = None
    project_uid: Optional[int] = None
    task_uid: Optional[int] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def remove_sensitive(self):
        self.group_uid = None
        self.project_uid = None
        self.task_uid = None


class PortKeys:
    number = "number"
    group_uid = "group_uid"
    project_uid = "project_uid"
    task_uid = "task_uid"
    description = "description"
    extra = "extra"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[PortKeys] = PortKeys()
assert lexicographical_members(keys, Port())
