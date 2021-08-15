# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class UpdateInfoQ:
    key: str
    value: str


@dataclass
class UpdateInfoValueQ:
    value: str
