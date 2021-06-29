# -*- coding: utf-8 -*-

from os import setgid, chown
from grp import getgrnam
from typing import Union


def get_group_id(group: Union[str, int]) -> int:
    if isinstance(group, str):
        info = getgrnam(group)
        gr_gid = info[2]
        assert isinstance(gr_gid, int)
        return gr_gid
    elif isinstance(group, int):
        return group
    else:
        raise TypeError(f"Unsupported type: {type(group).__name__}")


def set_group(group: Union[str, int]) -> None:
    setgid(get_group_id(group))


def change_group(path: str, group: Union[str, int]) -> None:
    chown(path, -1, get_group_id(group))
