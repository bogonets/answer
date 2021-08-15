# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from dataclasses import dataclass


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
