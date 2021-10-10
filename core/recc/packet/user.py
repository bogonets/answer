# -*- coding: utf-8 -*-

from dataclasses import dataclass
from hashlib import sha256
from typing import Optional
from datetime import datetime
from recc.packet.preference import PreferenceA


@dataclass
class UserExtraA:
    dark: Optional[bool] = None
    lang: Optional[str] = None
    timezone: Optional[str] = None


@dataclass
class UserA:
    username: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    is_admin: Optional[bool] = None
    extra: Optional[UserExtraA] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


@dataclass
class UpdateUserQ:
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    is_admin: Optional[bool] = None
    extra: Optional[UserExtraA] = None

    def strip(self):
        if self.nickname:
            self.nickname.strip()
        if self.email:
            self.email.strip()
        if self.phone1:
            self.phone1.strip()
        if self.phone2:
            self.phone2.strip()

    def empty_is_none(self):
        if not self.nickname:
            self.nickname = None
        if not self.email:
            self.email = None
        if not self.phone1:
            self.phone1 = None
        if not self.phone2:
            self.phone2 = None
        if not self.extra:
            self.extra = None


@dataclass
class SigninA:
    access: str
    refresh: str
    user: UserA
    preference: PreferenceA


@dataclass
class SignupQ:
    username: str
    password: str  # Perhaps the client encoded it with SHA256.
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    is_admin: Optional[bool] = None
    extra: Optional[UserExtraA] = None

    @staticmethod
    def encrypt_password(password: str, encoding="utf-8") -> str:
        return sha256(password.encode(encoding=encoding)).hexdigest()

    def strip(self):
        if self.username:
            self.username.strip()
        if self.password:
            self.password.strip()
        if self.nickname:
            self.nickname.strip()
        if self.email:
            self.email.strip()
        if self.phone1:
            self.phone1.strip()
        if self.phone2:
            self.phone2.strip()

    def empty_is_none(self):
        if not self.nickname:
            self.nickname = None
        if not self.email:
            self.email = None
        if not self.phone1:
            self.phone1 = None
        if not self.phone2:
            self.phone2 = None
        if not self.extra:
            self.extra = None


@dataclass
class UpdatePasswordQ:
    before: str
    after: str


@dataclass
class RefreshTokenA:
    access: str
