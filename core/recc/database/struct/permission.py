# -*- coding: utf-8 -*-

from typing import Optional, Any, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


@dataclass
class Permission:
    uid: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    r_layout: Optional[bool] = None
    w_layout: Optional[bool] = None
    r_storage: Optional[bool] = None
    w_storage: Optional[bool] = None
    r_manager: Optional[bool] = None
    w_manager: Optional[bool] = None
    r_graph: Optional[bool] = None
    w_graph: Optional[bool] = None
    r_member: Optional[bool] = None
    w_member: Optional[bool] = None
    r_setting: Optional[bool] = None
    w_setting: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def remove_sensitive(self):
        self.uid = None


class PermissionKeys:
    uid = "uid"
    name = "name"
    description = "description"
    extra = "extra"
    r_layout = "r_layout"
    w_layout = "w_layout"
    r_storage = "r_storage"
    w_storage = "w_storage"
    r_manager = "r_manager"
    w_manager = "w_manager"
    r_graph = "r_graph"
    w_graph = "w_graph"
    r_member = "r_member"
    w_member = "w_member"
    r_setting = "r_setting"
    w_setting = "w_setting"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[PermissionKeys] = PermissionKeys()
assert lexicographical_members(keys, Permission())
