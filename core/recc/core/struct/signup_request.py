# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass


@dataclass
class SignupRequest:
    username: str
    password: str  # Perhaps the client encoded it with SHA256.
    nickname: Optional[str] = None
    email: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
