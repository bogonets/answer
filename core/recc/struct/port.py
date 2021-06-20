# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from recc.struct._structure import _Structure


class Port(_Structure):
    def __init__(
        self,
        number: Optional[int] = None,
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        self.number = number
        self.group_uid = group_uid
        self.project_uid = project_uid
        self.task_uid = task_uid
        self.description = description
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
        self.kwargs = kwargs
