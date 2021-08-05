# -*- coding: utf-8 -*-

from typing import Optional, Final
from datetime import datetime
from recc.struct.structure_base import StructureBase
from recc.inspect.lexicographical_members import lexicographical_members


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


class InfoKeys:
    key = "key"
    value = "value"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[InfoKeys] = InfoKeys()
assert lexicographical_members(keys, Info())
