# -*- coding: utf-8 -*-

from typing import Optional, Any, List, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


@dataclass
class Project:
    uid: Optional[int] = None
    group_uid: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def remove_sensitive(self):
        self.uid = None
        self.group_uid = None


class ProjectKeys:
    uid = "uid"
    group_uid = "group_uid"
    slug = "slug"
    name = "name"
    description = "description"
    features = "features"
    extra = "extra"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[ProjectKeys] = ProjectKeys()
assert lexicographical_members(keys, Project())
