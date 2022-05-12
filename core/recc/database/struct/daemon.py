# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Daemon:
    uid: int
    plugin: str
    slug: str
    name: str
    address: str
    description: str
    enable: bool
    created_at: datetime
    updated_at: datetime
