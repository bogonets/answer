# -*- coding: utf-8 -*-

from dataclasses import dataclass

from recc.database.struct.port import Port

PortA = Port


@dataclass
class PortRangeA:
    min: int
    max: int
