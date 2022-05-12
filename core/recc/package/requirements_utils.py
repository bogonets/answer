# -*- coding: utf-8 -*-

import os
from functools import reduce
from typing import Iterable, List

_SCRIPT_PATH = os.path.abspath(__file__)
_RECC_PACKAGE_DIR = os.path.dirname(_SCRIPT_PATH)
_REQUIREMENTS_MAIN_PATH = os.path.join(_RECC_PACKAGE_DIR, "requirements.main.txt")


def _read_file(path: str, encoding="utf-8") -> str:
    with open(path, encoding=encoding) as f:
        return f.read()


def split_packages(content: str) -> List[str]:
    lines0 = content.split("\n")
    lines1 = map(lambda x: x.strip(), lines0)
    lines2 = filter(lambda x: x and x[0] != "#", lines1)
    return list(lines2)


def read_packages(path: str, encoding="utf-8") -> List[str]:
    return split_packages(_read_file(path, encoding))


def merge_requirements_argument(packages: Iterable[str]) -> str:
    args = [f"'{p}'" for p in packages if p]
    return reduce(lambda x, y: f"{x} {y}", args)


RECC_REQUIREMENTS_MAIN = read_packages(_REQUIREMENTS_MAIN_PATH)
RECC_REQUIREMENTS_MAIN_ARG = merge_requirements_argument(RECC_REQUIREMENTS_MAIN)
