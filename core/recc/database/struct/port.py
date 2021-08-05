# -*- coding: utf-8 -*-

from typing import Optional, Any, Final
from datetime import datetime
from recc.struct.structure_base import StructureBase
from recc.inspect.lexicographical_members import lexicographical_members


class Port(StructureBase):
    def __init__(
        self,
        number: Optional[int] = None,
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.number = number
        self.group_uid = group_uid
        self.project_uid = project_uid
        self.task_uid = task_uid
        self.description = description
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at


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
