# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Pip:
    domain: str
    name: str
    file: str
    hash_method: str
    hash_value: str
