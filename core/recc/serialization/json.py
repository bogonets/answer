# -*- coding: utf-8 -*-

import codecs
from typing import Type, TypeVar, Optional, Any, Final
from json import JSONDecodeError
from recc.driver.json import global_json_encoder, global_json_decoder
from recc.serialization.serialize import serialize
from recc.serialization.deserialize import deserialize

_T = TypeVar("_T")
_ET = TypeVar("_ET")

DEFAULT_ENCODING: Final[str] = "utf-8"


def _encode_json_text(data: Any) -> str:
    return global_json_encoder(data)


def _decode_json_text(json_text: str) -> Any:
    return global_json_decoder(json_text)


def serialize_json_text(version: int, obj: Any) -> str:
    return _encode_json_text(serialize(version, obj))


def deserialize_json_text(
    version: int,
    json_text: str,
    cls: Type[_T],
    hint: Optional[Type[_ET]] = None,
) -> Any:
    return deserialize(version, _decode_json_text(json_text), cls, hint)


def serialize_json_file(
    version: int,
    obj: Any,
    path: str,
    encoding=DEFAULT_ENCODING,
) -> None:
    with open(path, mode="w", encoding=encoding) as f:
        f.write(serialize_json_text(version, obj))


def deserialize_json_file(
    version: int,
    json_file: str,
    cls: Type[_T],
    hint: Optional[Type[_ET]] = None,
    encoding=DEFAULT_ENCODING,
) -> Any:
    try:
        with codecs.open(filename=json_file, encoding=encoding) as f:
            return deserialize_json_text(version, f.read(), cls, hint)
    except JSONDecodeError as e:
        msg = f"{json_file} file, {e.msg}"
        doc = e.doc
        pos = e.pos
        raise JSONDecodeError(msg, doc, pos)
