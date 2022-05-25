# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List

from recc.packet.plugin import PluginMenuA


@dataclass
class ExtraA:
    menus: Dict[str, List[PluginMenuA]]


@dataclass
class PreferenceA:
    oem: str
    extra: ExtraA
