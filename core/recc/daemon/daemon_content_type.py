# -*- coding: utf-8 -*-

from enum import Enum
from recc.proto.daemon.daemon_api_pb2 import ContentType


class DaemonContentType(Enum):
    Pickle5 = 0
    Json = 1
    JsonZlib = 2
    JsonGzip = 3
    JsonLzma = 4
    JsonBz2 = 5
    Msgpack = 6
    MsgpackZlib = 7
    MsgpackGzip = 8
    MsgpackLzma = 9
    MsgpackBz2 = 10


assert ContentType.Pickle5 == DaemonContentType.Pickle5.value
assert ContentType.Json == DaemonContentType.Json.value
assert ContentType.JsonZlib == DaemonContentType.JsonZlib.value
assert ContentType.JsonGzip == DaemonContentType.JsonGzip.value
assert ContentType.JsonLzma == DaemonContentType.JsonLzma.value
assert ContentType.JsonBz2 == DaemonContentType.JsonBz2.value
assert ContentType.Msgpack == DaemonContentType.Msgpack.value
assert ContentType.MsgpackZlib == DaemonContentType.MsgpackZlib.value
assert ContentType.MsgpackGzip == DaemonContentType.MsgpackGzip.value
assert ContentType.MsgpackLzma == DaemonContentType.MsgpackLzma.value
assert ContentType.MsgpackBz2 == DaemonContentType.MsgpackBz2.value
