# -*- coding: utf-8 -*-

from datetime import datetime
from dataclasses import dataclass


@dataclass
class SystemOverviewA:
    time: datetime
    users: int
    groups: int
    projects: int


@dataclass
class VersionsA:
    python: str
