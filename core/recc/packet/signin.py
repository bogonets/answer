# -*- coding: utf-8 -*-

from dataclasses import dataclass
from recc.database.struct.user import User


@dataclass
class SigninA:
    access: str
    refresh: str
    user: User
