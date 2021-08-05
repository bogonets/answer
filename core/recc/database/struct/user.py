# -*- coding: utf-8 -*-

from typing import Optional, Any, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


class PassInfo:
    password: str
    salt: str

    def __init__(self, password: str, salt: str, strip=True):
        if strip:
            self.password = password.strip()
            self.salt = salt.strip()
        else:
            self.password = password
            self.salt = salt


@dataclass
class User:
    uid: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    salt: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    is_admin: Optional[bool] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    def remove_sensitive(self):
        self.uid = None
        self.password = None
        self.salt = None


class UserKeys:
    uid = "uid"
    username = "username"
    password = "password"
    salt = "salt"
    nickname = "nickname"
    email = "email"
    phone1 = "phone1"
    phone2 = "phone2"
    is_admin = "is_admin"
    extra = "extra"
    created_at = "created_at"
    updated_at = "updated_at"
    last_login = "last_login"


keys: Final[UserKeys] = UserKeys()
assert lexicographical_members(keys, User())
