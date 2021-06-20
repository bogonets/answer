# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime
from recc.struct._structure import _Structure


class Info(_Structure):
    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        self.key = key
        self.value = value
        self.created_at = created_at
        self.updated_at = updated_at
        self.kwargs = kwargs
