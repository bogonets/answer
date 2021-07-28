# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from recc.struct.structure_base import StructureBase


class Group(StructureBase):
    def __init__(
        self,
        uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.uid = uid
        self.name = name
        self.description = description
        self.features = features
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
