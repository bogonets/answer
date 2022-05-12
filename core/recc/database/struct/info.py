# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Info:
    key: str
    value: str
    created_at: datetime
    updated_at: datetime
