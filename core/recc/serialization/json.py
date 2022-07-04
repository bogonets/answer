# -*- coding: utf-8 -*-

from typing import Any, Final, TypeVar

from type_serialize import serialize

from recc.driver.json import global_json_decoder, global_json_encoder

_T = TypeVar("_T")
_ET = TypeVar("_ET")

DEFAULT_ENCODING: Final[str] = "utf-8"


def _encode_json_text(data: Any) -> str:
    return global_json_encoder(data)


def _decode_json_text(json_text: str) -> Any:
    return global_json_decoder(json_text)


def serialize_json_text(obj: Any) -> str:
    return _encode_json_text(serialize(obj))


def serialize_json_file(
    obj: Any,
    path: str,
    encoding=DEFAULT_ENCODING,
) -> None:
    with open(path, mode="w", encoding=encoding) as f:
        f.write(serialize_json_text(obj))
