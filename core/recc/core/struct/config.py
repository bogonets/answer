# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Config:
    key: str
    type: str
    value: str


@dataclass
class UpdateConfigValue:
    value: str
