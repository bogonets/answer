# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


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

    def strip_insensitive(self):
        if self.nickname:
            self.nickname.strip()
        if self.email:
            self.email.strip()
        if self.phone1:
            self.phone1.strip()
        if self.phone2:
            self.phone2.strip()

    def empty_is_none_insensitive(self):
        if not self.nickname:
            self.nickname = None
        if not self.email:
            self.email = None
        if not self.phone1:
            self.phone1 = None
        if not self.phone2:
            self.phone2 = None
        if not self.is_admin:
            self.is_admin = None
        if not self.extra:
            self.extra = None
