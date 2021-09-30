# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class SystemOverviewA:
    users: int
    groups: int
    projects: int


@dataclass
class VersionsA:
    python: str
