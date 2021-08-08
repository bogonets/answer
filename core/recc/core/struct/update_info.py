# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class UpdateInfo:
    key: str
    value: str
