# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict


@dataclass
class PluginA:
    name: str


@dataclass
class PluginNameA:
    name: str


@dataclass
class PluginMenuA:
    icon: str
    name: str
    path: str
    lang: Dict[str, Dict[str, str]]
