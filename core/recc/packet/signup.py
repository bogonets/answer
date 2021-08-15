# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass
from hashlib import sha256


@dataclass
class SignupQ:
    username: str
    password: str  # Perhaps the client encoded it with SHA256.
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None

    @staticmethod
    def encrypt_password(password: str) -> str:
        return sha256(password.encode(encoding="utf-8")).hexdigest()
