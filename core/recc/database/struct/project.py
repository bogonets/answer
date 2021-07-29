# -*- coding: utf-8 -*-

from typing import Optional, Any, List, Final
from datetime import datetime
from recc.struct.structure_base import StructureBase
from recc.algorithm.lexicographical import lexicographical_equals


class Project(StructureBase):
    def __init__(
        self,
        uid: Optional[int] = None,
        group_uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.uid = uid
        self.group_uid = group_uid
        self.name = name
        self.description = description
        self.features = features
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at


class ProjectKeys:
    uid = "uid"
    group_uid = "group_uid"
    name = "name"
    description = "description"
    features = "features"
    extra = "extra"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[ProjectKeys] = ProjectKeys()
assert lexicographical_equals(keys, Project())
