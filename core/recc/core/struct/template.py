# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class TemplateKey:
    position: int
    category: str
    name: str
