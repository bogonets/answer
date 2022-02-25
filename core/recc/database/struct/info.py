# -*- coding: utf-8 -*-

from datetime import datetime
from dataclasses import dataclass


@dataclass
class Info:
    key: str
    value: str
    created_at: datetime
    updated_at: datetime
