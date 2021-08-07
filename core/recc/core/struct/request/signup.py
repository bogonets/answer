# -*- coding: utf-8 -*-

from typing import Optional, Final
from dataclasses import dataclass


@dataclass
class Signup:
    username: str
    password: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None


class SignupKeys:
    username = "username"
    password = "password"
    nickname = "nickname"
    email = "email"
    phone1 = "phone1"
    phone2 = "phone2"


keys: Final[SignupKeys] = SignupKeys()
