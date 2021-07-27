# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime
from recc.struct.structure_base import StructureBase


class Info(StructureBase):
    def __init__(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.key = key
        self.value = value
        self.created_at = created_at
        self.updated_at = updated_at
