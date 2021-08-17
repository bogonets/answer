# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class InfoA:
    key: str
    value: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateInfoQ:
    key: str
    value: str


@dataclass
class UpdateInfoQ:
    value: str
