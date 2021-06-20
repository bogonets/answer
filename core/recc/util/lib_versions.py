# -*- coding: utf-8 -*-

from google.protobuf import __version__ as protobuf_version_text
from grpc import __version__ as grpc_version_text
from uvloop import __version__ as uvloop_version_text
from orjson import __version__ as orjson_version_text
from jwt import __version__ as pyjwt_version_text  # noqa
from numpy import version as numpy_version_text


PROTOBUF_VERSION = protobuf_version_text
GRPC_VERSION = grpc_version_text
UVLOOP_VERSION = uvloop_version_text
ORJSON_VERSION = orjson_version_text
PYJWT_VERSION = pyjwt_version_text
NUMPY_VERSION = numpy_version_text
