# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from recc.struct.structure_base import StructureBase


class Project(StructureBase):
    def __init__(
        self,
        uid: Optional[int] = None,
        group_uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.uid = uid
        self.group_uid = group_uid
        self.name = name
        self.description = description
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
