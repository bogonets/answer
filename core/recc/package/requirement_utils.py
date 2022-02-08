# -*- coding: utf-8 -*-

import os
from typing import List, Iterable
from functools import reduce

RECC_REQUIREMENTS_MAIN = (
    "docker>=5.0.3",
    "aiohttp[speedups]>=3.7.3",
    "cchardet>=2.1.7",
    "aiodns>=3.0.0",
    "brotlipy>=0.7.0",
    "aiohttp_cors>=0.7.0",
    "aiohttp-swagger>=1.0.16",
    "grpcio>=1.43.0",
    "asyncpg>=0.25.0",
    "pyyaml>=6.0",
    "psutil>=5.9.0",
    "pyjwt>=2.3.0",
    "uvloop>=0.16.0",
    "async-timeout>=3.0.1",
    "aioredis>=2.0.1",
    "orjson>=3.6.6",
    "protobuf>=3.19.4",
    "numpy>=1.22.2",
    "colorama>=0.4.4",
    "coloredlogs>=15.0.1",
    "pycryptodome>=3.14.1",
    "overrides>=6.1.0",
    "xmltodict>=0.12.0",
    "minio>=7.1.3",
    "shapely>=1.8.0",
    "python-dateutil>=2.8.2",
    "msgpack>=1.0.3",
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
