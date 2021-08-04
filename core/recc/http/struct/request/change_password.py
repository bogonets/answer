# -*- coding: utf-8 -*-

from typing import Final


class ChangePassword:

    __slots__ = ("before", "after")

    def __init__(self, before: str, after: str):
        self.before = before
        self.after = after


class ChangePasswordKeys:
    before = "before"
    after = "after"


keys: Final[ChangePasswordKeys] = ChangePasswordKeys()
