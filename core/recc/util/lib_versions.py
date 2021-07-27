# -*- coding: utf-8 -*-

from typing import Final
from sys import version_info as python_version_info
from aiohttp import __version__ as aiohttp_version_text
from google.protobuf import __version__ as protobuf_version_text
from grpc import __version__ as grpc_version_text
from uvloop import __version__ as uvloop_version_text
from orjson import __version__ as orjson_version_text
from jwt import __version__ as pyjwt_version_text  # noqa
from numpy import version as numpy_version_text


PYTHON_MAJOR = python_version_info.major
PYTHON_MINOR = python_version_info.minor
PYTHON_MICRO = python_version_info.micro
PYTHON_RELEASE_LEVEL = python_version_info.releaselevel
PYTHON_SERIAL = python_version_info.serial
PYTHON_VERSION_TEXT = f"{PYTHON_MAJOR}.{PYTHON_MINOR}.{PYTHON_MICRO}"

PYTHON_VERSION: Final[str] = PYTHON_VERSION_TEXT
AIOHTTP_VERSION: Final[str] = aiohttp_version_text
PROTOBUF_VERSION: Final[str] = str(protobuf_version_text)
GRPC_VERSION: Final[str] = grpc_version_text
UVLOOP_VERSION: Final[str] = uvloop_version_text
ORJSON_VERSION: Final[str] = orjson_version_text
PYJWT_VERSION: Final[str] = pyjwt_version_text
NUMPY_VERSION: Final[str] = str(numpy_version_text)

assert isinstance(PYTHON_VERSION, str)
assert isinstance(AIOHTTP_VERSION, str)
assert isinstance(PROTOBUF_VERSION, str)
assert isinstance(GRPC_VERSION, str)
assert isinstance(UVLOOP_VERSION, str)
assert isinstance(ORJSON_VERSION, str)
assert isinstance(PYJWT_VERSION, str)
assert isinstance(NUMPY_VERSION, str)
