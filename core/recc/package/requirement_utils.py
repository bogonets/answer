# -*- coding: utf-8 -*-

import os
from typing import List, Iterable
from functools import reduce

RECC_REQUIREMENTS_MAIN = (
    "docker>=4.4.0",
    "aiohttp[speedups]>=3.7.3",
    "cchardet>=2.1.7",
    "aiodns>=2.0.0",
    "brotlipy>=0.7.0",
    "aiohttp_cors>=0.7.0",
    "grpcio>=1.36.1",
    "asyncpg>=0.22.0",
    "pyyaml>=5.4.1",
    "psutil>=5.8.0",
    "pyjwt>=2.0.1",
    "uvloop>=0.15.2",
    "aioredis>=1.3.1",
    "orjson>=3.5.1",
    "protobuf>=3.15.6",
    "numpy>=1.20.2",
    "colorama>=0.4.4",
    "coloredlogs>=15.0.1",
    "pycryptodome>=3.10.1",
)

_SCRIPT_PATH = os.path.abspath(__file__)
_CORE_RECC_PACKAGE_DIR = os.path.dirname(_SCRIPT_PATH)
_CORE_RECC_DIR = os.path.dirname(_CORE_RECC_PACKAGE_DIR)
_CORE_DIR = os.path.dirname(_CORE_RECC_DIR)
_CORE_REQUIREMENTS_MAIN_PATH = os.path.join(_CORE_DIR, "requirements.main.txt")


def _read_file(path: str, encoding="utf-8") -> str:
    with open(path, encoding=encoding) as f:
        return f.read()


def read_requirements(path: str, encoding="utf-8") -> List[str]:
    content = _read_file(path, encoding)
    lines0 = content.split("\n")
    lines1 = map(lambda x: x.strip(), lines0)
    lines2 = filter(lambda x: x and x[0] != "#", lines1)
    return list(lines2)


def read_requirements_main_from_source_file() -> List[str]:
    return read_requirements(_CORE_REQUIREMENTS_MAIN_PATH)


def get_requirements_argument(packages: Iterable[str]) -> str:
    args = [f"'{p}'" for p in packages if p]
    return reduce(lambda x, y: f"{x} {y}", args)


def get_recc_requirements_main_argument() -> str:
    return get_requirements_argument(RECC_REQUIREMENTS_MAIN)


RECC_REQUIREMENTS_MAIN_ARG = get_recc_requirements_main_argument()
