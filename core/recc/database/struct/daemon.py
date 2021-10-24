# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Daemon:
    uid: Optional[int] = None
    plugin: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    requirements_sha256: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    enable: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def remove_sensitive(self):
        self.uid = None
