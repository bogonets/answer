# -*- coding: utf-8 -*-

from typing import Dict, Union
from sys import version_info


PY_26 = version_info >= (2, 6)
PY_27 = version_info >= (2, 7)

PY_36 = version_info >= (3, 6)
PY_37 = version_info >= (3, 7)
PY_38 = version_info >= (3, 8)
PY_39 = version_info >= (3, 9)


def get_python_version_info() -> Dict[str, Union[int, str]]:
    return {
        "major": version_info[0],
        "minor": version_info[1],
        "micro": version_info[2],
        "releaselevel": version_info[3],
        "serial": version_info[4],
    }


def get_python_version_simple() -> str:
    return f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
