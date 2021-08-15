# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from dataclasses import dataclass


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

    def remove_sensitive(self) -> None:
        self.uid = None
        self.group_uid = None
