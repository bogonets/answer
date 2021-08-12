# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class TemplateKey:
    position: str
    category: str
    name: str
