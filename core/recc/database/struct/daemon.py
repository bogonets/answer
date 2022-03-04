# -*- coding: utf-8 -*-

from datetime import datetime
from dataclasses import dataclass


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
