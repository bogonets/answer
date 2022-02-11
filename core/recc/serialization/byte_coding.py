from enum import Enum

from typing import Any, Optional
from recc.serialization.serialize import serialize_default
from recc.serialization.deserialize import deserialize_default
from recc.serialization.byte import (
    DEFAULT_PICKLE_ENCODING,
    COMPRESS_LEVEL_TRADEOFF,
    pickling5,
    unpickling,
    orjson_encoder,
    orjson_decoder,
    orjson_zlib_encoder,
    orjson_zlib_decoder,
    orjson_gzip_encoder,
    orjson_gzip_decoder,
    orjson_lzma_encoder,
    orjson_lzma_decoder,
    orjson_bz2_encoder,
    orjson_bz2_decoder,
    msgpack_encoder,
    msgpack_decoder,
    msgpack_zlib_encoder,
    msgpack_zlib_decoder,
    msgpack_gzip_encoder,
    msgpack_gzip_decoder,
    msgpack_lzma_encoder,
    msgpack_lzma_decoder,
    msgpack_bz2_encoder,
    msgpack_bz2_decoder,
)


class ByteCodingType(Enum):
    Raw = 0
    Pickle5 = 1
    Json = 2
    JsonZlib = 3
    JsonGzip = 4
    JsonLzma = 5
    JsonBz2 = 6
    Msgpack = 7
    MsgpackZlib = 8
    MsgpackGzip = 9
    MsgpackLzma = 10
    MsgpackBz2 = 11


def object_to_bytes(
    data: Any,
    coding: ByteCodingType,
    *,
    level=COMPRESS_LEVEL_TRADEOFF,
) -> bytes:
    if coding == ByteCodingType.Raw:
        raise ValueError("Unsupported raw packet type")
    elif coding == ByteCodingType.Pickle5:
        return pickling5(data)
    elif coding == ByteCodingType.Json:
        return orjson_encoder(data)
    elif coding == ByteCodingType.JsonZlib:
        return orjson_zlib_encoder(data, level)
    elif coding == ByteCodingType.JsonGzip:
        return orjson_gzip_encoder(data, level)
    elif coding == ByteCodingType.JsonLzma:
        return orjson_lzma_encoder(data)
    elif coding == ByteCodingType.JsonBz2:
        return orjson_bz2_encoder(data, level)
    elif coding == ByteCodingType.Msgpack:
        return msgpack_encoder(data)
    elif coding == ByteCodingType.MsgpackZlib:
        return msgpack_zlib_encoder(data, level)
    elif coding == ByteCodingType.MsgpackGzip:
        return msgpack_gzip_encoder(data, level)
    elif coding == ByteCodingType.MsgpackLzma:
        return msgpack_lzma_encoder(data)
    elif coding == ByteCodingType.MsgpackBz2:
        return msgpack_bz2_encoder(data, level)
    else:
        raise ValueError(f"Unknown packet type: {coding}")


def bytes_to_object(
    data: bytes,
    coding: ByteCodingType,
    *,
    encoding=DEFAULT_PICKLE_ENCODING,
) -> Any:
    if coding == ByteCodingType.Raw:
        raise ValueError("Unsupported raw packet type")
    elif coding == ByteCodingType.Pickle5:
        return unpickling(data, encoding)
    elif coding == ByteCodingType.Json:
        return orjson_decoder(data)
    elif coding == ByteCodingType.JsonZlib:
        return orjson_zlib_decoder(data)
    elif coding == ByteCodingType.JsonGzip:
        return orjson_gzip_decoder(data)
    elif coding == ByteCodingType.JsonLzma:
        return orjson_lzma_decoder(data)
    elif coding == ByteCodingType.JsonBz2:
        return orjson_bz2_decoder(data)
    elif coding == ByteCodingType.Msgpack:
        return msgpack_decoder(data)
    elif coding == ByteCodingType.MsgpackZlib:
        return msgpack_zlib_decoder(data)
    elif coding == ByteCodingType.MsgpackGzip:
        return msgpack_gzip_decoder(data)
    elif coding == ByteCodingType.MsgpackLzma:
        return msgpack_lzma_decoder(data)
    elif coding == ByteCodingType.MsgpackBz2:
        return msgpack_bz2_decoder(data)
    else:
        raise ValueError(f"Unknown packet type: {coding}")


def encode(
    data: Any,
    coding: ByteCodingType,
    *,
    level=COMPRESS_LEVEL_TRADEOFF,
) -> bytes:
    return object_to_bytes(
        data=serialize_default(data),
        coding=coding,
        level=level,
    )


def decode(
    data: bytes,
    coding: ByteCodingType,
    cls: Optional[Any] = None,
    *,
    encoding=DEFAULT_PICKLE_ENCODING,
) -> Any:
    obj = bytes_to_object(data=data, coding=coding, encoding=encoding)
    return deserialize_default(obj, cls) if cls is not None else obj
