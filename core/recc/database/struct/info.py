# -*- coding: utf-8 -*-

from typing import Optional, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


@dataclass
class Info:
    key: Optional[str] = None
    value: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class InfoKeys:
    key = "key"
    value = "value"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[InfoKeys] = InfoKeys()
assert lexicographical_members(keys, Info())
