# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class SystemOverview:
    users: int
    groups: int
    projects: int
