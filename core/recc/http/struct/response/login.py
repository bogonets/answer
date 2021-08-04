# -*- coding: utf-8 -*-

from typing import Final
from recc.database.struct.user import User


class Login:

    __slots__ = ("access", "refresh", "user")

    def __init__(self, access: str, refresh: str, user: User):
        self.access = access
        self.refresh = refresh
        self.user = user


class LoginKeys:
    access = "access"
    refresh = "refresh"
    user = "user"


keys: Final[LoginKeys] = LoginKeys()
