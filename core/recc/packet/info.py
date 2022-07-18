# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Info:
    """It is mapped to the `info` table in the database."""

    key: str
    value: str
    created_at: datetime
    updated_at: datetime


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
