# -*- coding: utf-8 -*-

from os import setuid, chown
from pwd import getpwnam
from typing import Union


def get_user_id(user: Union[str, int]) -> int:
    if isinstance(user, str):
        info = getpwnam(user)
        pw_uid = info[2]
        assert isinstance(pw_uid, int)
        return pw_uid
    elif isinstance(user, int):
        return user
    else:
        raise TypeError(f"Unsupported type: {type(user).__name__}")


def set_user(user: Union[str, int]) -> None:
    setuid(get_user_id(user))


def change_user(path: str, user: Union[str, int]) -> None:
    chown(path, get_user_id(user), -1)
