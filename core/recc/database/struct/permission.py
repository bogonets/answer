# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


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
