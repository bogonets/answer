# -*- coding: utf-8 -*-

import pickle
import orjson
import zlib
import gzip
import lzma
import bz2
from typing import Any, Callable
from recc.variables.rpc import (
    DEFAULT_PICKLE_PROTOCOL_VERSION,
    DEFAULT_PICKLE_ENCODING,
)

ByteEncoder = Callable[[Any], bytes]
ByteDecoder = Callable[[bytes], Any]

COMPRESS_LEVEL_FAST = 1
COMPRESS_LEVEL_TRADEOFF = 6
COMPRESS_LEVEL_BEST = 9


def pickling(data: Any, protocol=DEFAULT_PICKLE_PROTOCOL_VERSION) -> bytes:
    return pickle.dumps(data, protocol=protocol)


def unpickling(data: bytes, encoding=DEFAULT_PICKLE_ENCODING) -> Any:
    return pickle.loads(data, encoding=encoding)


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
