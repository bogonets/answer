# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PluginMenuA:
    icon: str
    name: str
    path: str
    translations: Dict[str, str]
    permission: str


@dataclass
class PluginMenusA:
    admin: List[PluginMenuA]
    group: List[PluginMenuA]
    project: List[PluginMenuA]
    user: List[PluginMenuA]


@dataclass
class PluginA:
    name: str
    menus: PluginMenusA


@dataclass
class PluginNameA:
    name: str
