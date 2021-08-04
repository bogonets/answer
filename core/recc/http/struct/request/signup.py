# -*- coding: utf-8 -*-

from typing import Optional, Final


class Signup:

    __slots__ = ("username", "password", "email", "phone1", "phone2")

    def __init__(
        self,
        username: str,
        password: str,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
    ):
        self.username = username
        self.password = password
        self.email = email
        self.phone1 = phone1
        self.phone2 = phone2


class SignupKeys:
    username = "username"
    password = "password"
    email = "email"
    phone1 = "phone1"
    phone2 = "phone2"


keys: Final[SignupKeys] = SignupKeys()
