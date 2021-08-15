# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Info:
    key: Optional[str] = None
    value: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
