# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from recc.struct._structure import _Structure


class Permission(_Structure):
    def __init__(
        self,
        uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        r_layout: Optional[bool] = None,
        w_layout: Optional[bool] = None,
        r_storage: Optional[bool] = None,
        w_storage: Optional[bool] = None,
        r_manager: Optional[bool] = None,
        w_manager: Optional[bool] = None,
        r_graph: Optional[bool] = None,
        w_graph: Optional[bool] = None,
        r_member: Optional[bool] = None,
        w_member: Optional[bool] = None,
        r_setting: Optional[bool] = None,
        w_setting: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        self.uid = uid
        self.name = name
        self.description = description
        self.extra = extra
        self.r_layout = r_layout
        self.w_layout = w_layout
        self.r_storage = r_storage
        self.w_storage = w_storage
        self.r_manager = r_manager
        self.w_manager = w_manager
        self.r_graph = r_graph
        self.w_graph = w_graph
        self.r_member = r_member
        self.w_member = w_member
        self.r_setting = r_setting
        self.w_setting = w_setting
        self.created_at = created_at
        self.updated_at = updated_at
        self.kwargs = kwargs
