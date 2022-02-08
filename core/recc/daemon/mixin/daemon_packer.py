# -*- coding: utf-8 -*-

from typing import Any, Optional
from recc.daemon.daemon_content_type import DaemonContentType
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
from recc.serialization.serialize import serialize_default
from recc.serialization.deserialize import deserialize_default


class DaemonPacker:
    @staticmethod
    def object_to_bytes(
        data: Any,
        content_type: DaemonContentType,
        *,
        level=COMPRESS_LEVEL_TRADEOFF,
    ) -> bytes:
        if content_type == DaemonContentType.Pickle5:
            return pickling5(data)
        elif content_type == DaemonContentType.Json:
            return orjson_encoder(data)
        elif content_type == DaemonContentType.JsonZlib:
            return orjson_zlib_encoder(data, level)
        elif content_type == DaemonContentType.JsonGzip:
            return orjson_gzip_encoder(data, level)
        elif content_type == DaemonContentType.JsonLzma:
            return orjson_lzma_encoder(data)
        elif content_type == DaemonContentType.JsonBz2:
            return orjson_bz2_encoder(data, level)
        elif content_type == DaemonContentType.Msgpack:
            return msgpack_encoder(data)
        elif content_type == DaemonContentType.MsgpackZlib:
            return msgpack_zlib_encoder(data, level)
        elif content_type == DaemonContentType.MsgpackGzip:
            return msgpack_gzip_encoder(data, level)
        elif content_type == DaemonContentType.MsgpackLzma:
            return msgpack_lzma_encoder(data)
        elif content_type == DaemonContentType.MsgpackBz2:
            return msgpack_bz2_encoder(data, level)
        else:
            raise ValueError(f"Unknown packet type: {content_type}")

    @staticmethod
    def bytes_to_object(
        data: bytes,
        content_type: DaemonContentType,
        *,
        encoding=DEFAULT_PICKLE_ENCODING,
    ) -> Any:
        if content_type == DaemonContentType.Pickle5:
            return unpickling(data, encoding)
        elif content_type == DaemonContentType.Json:
            return orjson_decoder(data)
        elif content_type == DaemonContentType.JsonZlib:
            return orjson_zlib_decoder(data)
        elif content_type == DaemonContentType.JsonGzip:
            return orjson_gzip_decoder(data)
        elif content_type == DaemonContentType.JsonLzma:
            return orjson_lzma_decoder(data)
        elif content_type == DaemonContentType.JsonBz2:
            return orjson_bz2_decoder(data)
        elif content_type == DaemonContentType.Msgpack:
            return msgpack_decoder(data)
        elif content_type == DaemonContentType.MsgpackZlib:
            return msgpack_zlib_decoder(data)
        elif content_type == DaemonContentType.MsgpackGzip:
            return msgpack_gzip_decoder(data)
        elif content_type == DaemonContentType.MsgpackLzma:
            return msgpack_lzma_decoder(data)
        elif content_type == DaemonContentType.MsgpackBz2:
            return msgpack_bz2_decoder(data)
        else:
            raise ValueError(f"Unknown packet type: {content_type}")

    @staticmethod
    def encode(
        data: Any,
        content_type: DaemonContentType,
        *,
        level=COMPRESS_LEVEL_TRADEOFF,
    ) -> bytes:
        return DaemonPacker.object_to_bytes(
            data=serialize_default(data),
            content_type=content_type,
            level=level,
        )

    @staticmethod
    def decode(
        data: bytes,
        content_type: DaemonContentType,
        cls: Optional[Any] = None,
        *,
        encoding=DEFAULT_PICKLE_ENCODING,
    ) -> Any:
        obj = DaemonPacker.bytes_to_object(
            data=data,
            content_type=content_type,
            encoding=encoding,
        )
        return deserialize_default(obj, cls) if cls is not None else obj
