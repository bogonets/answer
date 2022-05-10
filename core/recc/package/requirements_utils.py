# -*- coding: utf-8 -*-

import os
from typing import List, Iterable
from functools import reduce, lru_cache

_SCRIPT_PATH = os.path.abspath(__file__)
_RECC_PACKAGE_DIR = os.path.dirname(_SCRIPT_PATH)
_REQUIREMENTS_MAIN_PATH = os.path.join(_RECC_PACKAGE_DIR, "requirements.main.txt")


def _read_file(path: str, encoding="utf-8") -> str:
    with open(path, encoding=encoding) as f:
        return f.read()


def _read_requirements(path: str, encoding="utf-8") -> List[str]:
    content = _read_file(path, encoding)
    lines0 = content.split("\n")
    lines1 = map(lambda x: x.strip(), lines0)
    lines2 = filter(lambda x: x and x[0] != "#", lines1)
    return list(lines2)


RECC_REQUIREMENTS_MAIN = _read_requirements(_REQUIREMENTS_MAIN_PATH)


def get_requirements_argument(packages: Iterable[str]) -> str:
    args = [f"'{p}'" for p in packages if p]
    return reduce(lambda x, y: f"{x} {y}", args)


@lru_cache
def get_recc_requirements_main_argument() -> str:
    return get_requirements_argument(RECC_REQUIREMENTS_MAIN)


RECC_REQUIREMENTS_MAIN_ARG = get_recc_requirements_main_argument()
