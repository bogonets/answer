# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DaemonA:
    plugin: str
    slug: str
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    enable: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    status: Optional[str] = None
    exit_code: Optional[int] = None


@dataclass
class CreateDaemonQ:
    plugin: str
    slug: str
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    enable: bool = False


@dataclass
class UpdateDaemonQ:
    slug: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    enable: Optional[bool] = False
