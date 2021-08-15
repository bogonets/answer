# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class UpdatePasswordQ:
    before: str
    after: str
