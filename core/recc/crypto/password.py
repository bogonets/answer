# -*- coding: utf-8 -*-

from hashlib import pbkdf2_hmac
from recc.variables.crypto import (
    DEFAULT_PBKDF2_HMAC_HASH_NAME,
    DEFAULT_PBKDF2_HMAC_ITERATIONS,
)


def encrypt_password(hashed_user_pw: str, salt: bytes) -> bytes:
    return pbkdf2_hmac(
        DEFAULT_PBKDF2_HMAC_HASH_NAME,
        bytes.fromhex(hashed_user_pw),
        salt,
        DEFAULT_PBKDF2_HMAC_ITERATIONS,
    )
