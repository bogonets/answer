# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ChangePasswordRequest:
    before: str
    after: str
