# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import Optional

from recc.packet.preference import PreferenceA


@dataclass
class User:
    """It is mapped to the `user` table in the database."""

    uid: int
    username: str
    password: str
    salt: str

    nickname: str
    email: Optional[str]
    phone: Optional[str]
    admin: bool

    dark: int
    lang: str
    timezone: str

    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]


@dataclass
class UserInfo:
    """It is mapped to the `user_info` table in the database."""

    user_uid: int
    key: str
    value: str
    created_at: datetime
    updated_at: datetime


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
class UserA:
    username: str

    nickname: str
    email: str
    phone: str
    admin: bool

    dark: int
    lang: str
    timezone: str

    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    @classmethod
    def from_database(cls, user: User):
        return cls(
            username=user.username,
            nickname=user.nickname,
            email=user.email if user.email else str(),
            phone=user.phone if user.phone else str(),
            admin=user.admin,
            dark=user.dark,
            lang=user.lang,
            timezone=user.timezone,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
        )


@dataclass
class UserInfoA:
    key: str
    value: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_database(cls, info: UserInfo):
        return cls(
            key=info.key,
            value=info.value,
            created_at=info.created_at,
            updated_at=info.updated_at,
        )


@dataclass
class UpdateUserQ:
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    admin: Optional[bool] = None
    dark: Optional[int] = None
    lang: Optional[str] = None
    timezone: Optional[str] = None

    def strip(self):
        if self.nickname:
            self.nickname.strip()
        if self.email:
            self.email.strip()
        if self.phone:
            self.phone.strip()
        if self.lang:
            self.lang.strip()
        if self.timezone:
            self.timezone.strip()


@dataclass
class UpdateUserInfoQ:
    value: str


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
    phone: Optional[str] = None
    admin: Optional[bool] = None
    dark: Optional[int] = None
    lang: Optional[str] = None
    timezone: Optional[str] = None

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
        if self.phone:
            self.phone.strip()
        if self.lang:
            self.lang.strip()
        if self.timezone:
            self.timezone.strip()


@dataclass
class UpdatePasswordQ:
    before: str
    after: str


@dataclass
class RefreshTokenA:
    access: str
