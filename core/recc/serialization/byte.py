# -*- coding: utf-8 -*-

import zlib
import gzip
import lzma
import bz2

import pickle
import orjson
import msgpack

from typing import Any, Callable

ByteEncoder = Callable[[Any], bytes]
ByteDecoder = Callable[[bytes], Any]

DEFAULT_PICKLE_PROTOCOL_VERSION = 5
DEFAULT_PICKLE_ENCODING = "ASCII"

COMPRESS_LEVEL_FAST = 1
COMPRESS_LEVEL_TRADEOFF = 6
COMPRESS_LEVEL_BEST = 9


def pickling(data: Any, protocol=DEFAULT_PICKLE_PROTOCOL_VERSION) -> bytes:
    return pickle.dumps(data, protocol=protocol)


def pickling5(data: Any) -> bytes:
    return pickle.dumps(data, protocol=5)


def unpickling(data: bytes, encoding=DEFAULT_PICKLE_ENCODING) -> Any:
    return pickle.loads(data, encoding=encoding)


# ------
# orjson
# ------


def orjson_encoder(data: Any) -> bytes:
    return orjson.dumps(data)


def orjson_decoder(data: bytes) -> Any:
    return orjson.loads(data)


def orjson_zlib_encoder(data: Any, level=COMPRESS_LEVEL_BEST) -> bytes:
    assert 0 <= level <= 9 or level == -1
    return zlib.compress(orjson.dumps(data), level=level)


def orjson_zlib_decoder(data: bytes) -> Any:
    return orjson.loads(zlib.decompress(data))


def orjson_gzip_encoder(data: Any, level=COMPRESS_LEVEL_BEST) -> bytes:
    assert 0 <= level <= 9
    return gzip.compress(orjson.dumps(data), compresslevel=level)


def orjson_gzip_decoder(data: bytes) -> Any:
    return orjson.loads(gzip.decompress(data))


def orjson_lzma_encoder(data: Any) -> bytes:
    return lzma.compress(orjson.dumps(data))


def orjson_lzma_decoder(data: bytes) -> Any:
    return orjson.loads(lzma.decompress(data))


def orjson_bz2_encoder(data: Any, level=COMPRESS_LEVEL_BEST) -> bytes:
    assert 1 <= level <= 9
    return bz2.compress(orjson.dumps(data), compresslevel=level)


def orjson_bz2_decoder(data: bytes) -> Any:
    return orjson.loads(bz2.decompress(data))


# -------
# msgpack
# -------


def msgpack_encoder(data: Any) -> bytes:
    return msgpack.dumps(data)


def msgpack_decoder(data: bytes) -> Any:
    return msgpack.loads(data)


def msgpack_zlib_encoder(data: Any, level=COMPRESS_LEVEL_BEST) -> bytes:
    assert 0 <= level <= 9 or level == -1
    return zlib.compress(msgpack.dumps(data), level=level)


def msgpack_zlib_decoder(data: bytes) -> Any:
    return msgpack.loads(zlib.decompress(data))


def msgpack_gzip_encoder(data: Any, level=COMPRESS_LEVEL_BEST) -> bytes:
    assert 0 <= level <= 9
    return gzip.compress(msgpack.dumps(data), compresslevel=level)


def msgpack_gzip_decoder(data: bytes) -> Any:
    return msgpack.loads(gzip.decompress(data))


def msgpack_lzma_encoder(data: Any) -> bytes:
    return lzma.compress(msgpack.dumps(data))


def msgpack_lzma_decoder(data: bytes) -> Any:
    return msgpack.loads(lzma.decompress(data))


def msgpack_bz2_encoder(data: Any, level=COMPRESS_LEVEL_BEST) -> bytes:
    assert 1 <= level <= 9
    return bz2.compress(msgpack.dumps(data), compresslevel=level)


def msgpack_bz2_decoder(data: bytes) -> Any:
    return msgpack.loads(bz2.decompress(data))
