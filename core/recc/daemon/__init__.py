# -*- coding: utf-8 -*-

from type_serialize import ByteCoding

from recc.proto.daemon.daemon_api_pb2 import Coding

assert Coding.Raw == ByteCoding.Raw.value
assert Coding.Pickle5 == ByteCoding.Pickle5.value
assert Coding.Json == ByteCoding.Json.value
assert Coding.JsonZlib == ByteCoding.JsonZlib.value
assert Coding.JsonGzip == ByteCoding.JsonGzip.value
assert Coding.JsonLzma == ByteCoding.JsonLzma.value
assert Coding.JsonBz2 == ByteCoding.JsonBz2.value
assert Coding.Pyjson == ByteCoding.Pyjson.value
assert Coding.PyjsonZlib == ByteCoding.PyjsonZlib.value
assert Coding.PyjsonGzip == ByteCoding.PyjsonGzip.value
assert Coding.PyjsonLzma == ByteCoding.PyjsonLzma.value
assert Coding.PyjsonBz2 == ByteCoding.PyjsonBz2.value
assert Coding.Orjson == ByteCoding.Orjson.value
assert Coding.OrjsonZlib == ByteCoding.OrjsonZlib.value
assert Coding.OrjsonGzip == ByteCoding.OrjsonGzip.value
assert Coding.OrjsonLzma == ByteCoding.OrjsonLzma.value
assert Coding.OrjsonBz2 == ByteCoding.OrjsonBz2.value
assert Coding.Msgpack == ByteCoding.Msgpack.value
assert Coding.MsgpackZlib == ByteCoding.MsgpackZlib.value
assert Coding.MsgpackGzip == ByteCoding.MsgpackGzip.value
assert Coding.MsgpackLzma == ByteCoding.MsgpackLzma.value
assert Coding.MsgpackBz2 == ByteCoding.MsgpackBz2.value
assert Coding.Yaml == ByteCoding.Yaml.value
assert Coding.YamlZlib == ByteCoding.YamlZlib.value
assert Coding.YamlGzip == ByteCoding.YamlGzip.value
assert Coding.YamlLzma == ByteCoding.YamlLzma.value
assert Coding.YamlBz2 == ByteCoding.YamlBz2.value
