# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from recc.daemon.daemon_state import DaemonState


@dataclass
class DaemonA:
    plugin: str
    slug: str
    name: str
    address: str
    description: str
    enable: bool
    created_at: datetime
    updated_at: datetime

    state: DaemonState
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
