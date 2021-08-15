# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ConfigA:
    key: str
    type: str
    value: str


@dataclass
class UpdateConfigValueQ:
    value: str
