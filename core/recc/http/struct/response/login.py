# -*- coding: utf-8 -*-

from typing import Final, Optional
from dataclasses import dataclass
from recc.database.struct.user import User


@dataclass
class Login:
    access: str
    refresh: str
    user: Optional[User]


class LoginKeys:
    access = "access"
    refresh = "refresh"
    user = "user"


keys: Final[LoginKeys] = LoginKeys()
