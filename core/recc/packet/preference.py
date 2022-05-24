# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict


@dataclass
class ExtraMenuA:
    icon: str
    name: str
    plugin: str
    path: str
    translations: Dict[str, Dict[str, str]]


@dataclass
class PreferenceA:
    oem: str

    # self_menus: List[ExtraMenuA]
    # group_menus: List[ExtraMenuA]
    # project_menus: List[ExtraMenuA]
    # admin_menus: List[ExtraMenuA]
