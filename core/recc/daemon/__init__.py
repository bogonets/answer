# -*- coding: utf-8 -*-

from recc.proto.daemon.daemon_api_pb2 import Coding
from recc.serialization.byte_coding import ByteCodingType

assert Coding.Raw == ByteCodingType.Raw.value
assert Coding.Pickle5 == ByteCodingType.Pickle5.value
assert Coding.Json == ByteCodingType.Json.value
assert Coding.JsonZlib == ByteCodingType.JsonZlib.value
assert Coding.JsonGzip == ByteCodingType.JsonGzip.value
assert Coding.JsonLzma == ByteCodingType.JsonLzma.value
assert Coding.JsonBz2 == ByteCodingType.JsonBz2.value
assert Coding.Msgpack == ByteCodingType.Msgpack.value
assert Coding.MsgpackZlib == ByteCodingType.MsgpackZlib.value
assert Coding.MsgpackGzip == ByteCodingType.MsgpackGzip.value
assert Coding.MsgpackLzma == ByteCodingType.MsgpackLzma.value
assert Coding.MsgpackBz2 == ByteCodingType.MsgpackBz2.value
