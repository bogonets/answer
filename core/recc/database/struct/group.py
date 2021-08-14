# -*- coding: utf-8 -*-

from typing import Optional, Any, List, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


@dataclass
class Group:
    uid: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def remove_sensitive(self):
        self.uid = None


class GroupKeys:
    uid = "uid"
    slug = "slug"
    name = "name"
    description = "description"
    features = "features"
    extra = "extra"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[GroupKeys] = GroupKeys()
assert lexicographical_members(keys, Group())
