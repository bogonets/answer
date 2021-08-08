# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class UpdatePassword:
    before: str
    after: str
