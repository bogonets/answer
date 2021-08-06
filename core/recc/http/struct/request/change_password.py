# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ChangePassword:
    before: str
    after: str
