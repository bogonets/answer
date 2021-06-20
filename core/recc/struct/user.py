# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from recc.struct._structure import _Structure


class PassInfo:

    __slots__ = ("password", "salt")

    def __init__(self, password: str, salt: str, strip=True):
        if strip:
            self.password = password.strip()
            self.salt = salt.strip()
        else:
            self.password = password
            self.salt = salt


class User(_Structure):
    def __init__(
        self,
        uid: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        salt: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin: Optional[bool] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None,
        **kwargs,
    ):
        self.uid = uid
        self.username = username
        self.password = password
        self.salt = salt
        self.email = email
        self.phone1 = phone1
        self.phone2 = phone2
        self.is_admin = is_admin
        self.extra = extra
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_login = last_login
        self.kwargs = kwargs
