# -*- coding: utf-8 -*-

from typing import Final
from dataclasses import dataclass


@dataclass
class ChangePassword:
    before: str
    after: str


class ChangePasswordKeys:
    before = "before"
    after = "after"


keys: Final[ChangePasswordKeys] = ChangePasswordKeys()
