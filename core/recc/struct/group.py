# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from recc.struct._structure import _Structure


class Group(_Structure):
    def __init__(
        self,
        uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        self.uid = uid
        self.name = name
        self.description = description
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
        self.kwargs = kwargs
