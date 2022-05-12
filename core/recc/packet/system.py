# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime


@dataclass
class SystemOverviewA:
    time: datetime
    users: int
    groups: int
    projects: int


@dataclass
class VersionsA:
    python: str
