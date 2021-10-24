# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class DaemonA:
    plugin: str
    name: str
    address: Optional[str] = None
    requirements_sha256: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    enable: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    running: Optional[bool] = None
    exit_code: Optional[int] = None


@dataclass
class CreateDaemonQ:
    plugin: str
    name: str
    address: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    enable: bool = False


@dataclass
class UpdateDaemonQ:
    name: str
    address: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    enable: Optional[bool] = False
