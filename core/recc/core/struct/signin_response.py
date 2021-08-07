# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass
from recc.database.struct.user import User


@dataclass
class SigninResponse:
    access: str
    refresh: str
    user: Optional[User]
