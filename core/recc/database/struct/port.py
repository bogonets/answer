# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Port:
    number: Optional[int] = None
    group_uid: Optional[int] = None
    project_uid: Optional[int] = None
    task_uid: Optional[int] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def remove_sensitive(self):
        self.group_uid = None
        self.project_uid = None
        self.task_uid = None
