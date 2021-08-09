# -*- coding: utf-8 -*-

from re import compile as re_compile

_RECC_KEY_PATTERN = r"^recc\..*"
_RECC_KEY_REGEX = re_compile(_RECC_KEY_PATTERN)


def valid_user_creatable(key: str) -> bool:
    return _RECC_KEY_REGEX.match(key) is None


def valid_user_modifiable(key: str) -> bool:
    return _RECC_KEY_REGEX.match(key) is None


def valid_user_removable(key: str) -> bool:
    return _RECC_KEY_REGEX.match(key) is None
