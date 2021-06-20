# -*- coding: utf-8 -*-

from typing import Any, Callable
import json


JsonByteEncoder = Callable[[Any], bytes]
JsonByteDecoder = Callable[[bytes], Any]
JsonEncoder = Callable[[Any], str]
JsonDecoder = Callable[[str], Any]


def python_json_byte_encoder(data: Any) -> bytes:
    return json.dumps(data).encode("utf-8")


def python_json_byte_decoder(data: bytes) -> Any:
    return json.loads(data)


def python_json_encoder(data: Any) -> str:
    return json.dumps(data)


def python_json_decoder(data: str) -> Any:
    return json.loads(data)


_global_json_byte_encoder: JsonByteEncoder = python_json_byte_encoder
_global_json_byte_decoder: JsonByteDecoder = python_json_byte_decoder
_global_json_encoder: JsonEncoder = python_json_encoder
_global_json_decoder: JsonDecoder = python_json_decoder


def install_orjson_driver() -> bool:
    """
    Install orjson driver.

    .. warning::
        It should not be applied to be installed automatically.
        If you find a driver error, you should use the Python default settings.
    """

    try:
        import orjson

        global _global_json_byte_encoder
        global _global_json_byte_decoder
        global _global_json_encoder
        global _global_json_decoder

        def orjson_byte_encoder(data: Any) -> bytes:
            return orjson.dumps(data)

        def orjson_byte_decoder(data: bytes) -> Any:
            return orjson.loads(data)

        def orjson_encoder(data: Any) -> str:
            return str(orjson.dumps(data), "utf-8")

        def orjson_decoder(data: str) -> Any:
            return orjson.loads(data)

        _global_json_byte_encoder = orjson_byte_encoder
        _global_json_byte_decoder = orjson_byte_decoder
        _global_json_encoder = orjson_encoder
        _global_json_decoder = orjson_decoder

        return True
    except ImportError:
        return False


def global_json_byte_encoder(data: Any) -> bytes:
    return _global_json_byte_encoder(data)


def global_json_byte_decoder(data: bytes) -> Any:
    return _global_json_byte_decoder(data)


def global_json_encoder(data: Any) -> str:
    return _global_json_encoder(data)


def global_json_decoder(data: str) -> Any:
    return _global_json_decoder(data)
