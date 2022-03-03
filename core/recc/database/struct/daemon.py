# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Daemon:
    uid: int
    plugin: str
    slug: str
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    enable: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
