# -*- coding: utf-8 -*-

from typing import Any, List, Optional, Iterable, Dict, Final
from recc.serialization.interface import (
    SerializeInterface,
    DeserializeInterface,
    SERIALIZE_METHOD_NAME,
    DESERIALIZE_METHOD_NAME,
)

MAPPING_METHOD_ITEMS: Final[str] = "items"
MAPPING_METHOD_KEYS: Final[str] = "keys"
SEQUENCE_METHOD_INSERT: Final[str] = "insert"


def is_serialize_cls(cls: Any) -> bool:
    if not isinstance(cls, type):
        return False
    if issubclass(cls, SerializeInterface):
        return True
    return hasattr(cls, SERIALIZE_METHOD_NAME)


def is_serialize_obj(obj: Any) -> bool:
    if isinstance(obj, type):
        return False
    if isinstance(obj, SerializeInterface):
        return True
    return hasattr(obj, SERIALIZE_METHOD_NAME)


def is_deserialize_cls(cls: Any) -> bool:
    if not isinstance(cls, type):
        return False
    if issubclass(cls, DeserializeInterface):
        return True
    return hasattr(cls, DESERIALIZE_METHOD_NAME)


def is_deserialize_obj(obj: Any) -> bool:
    if isinstance(obj, type):
        return False
    if isinstance(obj, DeserializeInterface):
        return True
    return hasattr(obj, DESERIALIZE_METHOD_NAME)


def is_serializable_pod_cls(cls: Any) -> bool:
    if not isinstance(cls, type):
        return False
    return issubclass(cls, int) or issubclass(cls, float) or issubclass(cls, str)


def is_serializable_pod_obj(obj: Any) -> bool:
    if isinstance(obj, type):
        return False
    return isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str)


def is_none(obj: Any) -> bool:
    if isinstance(obj, type):
        return issubclass(obj, type(None))
    else:
        return obj is None


def update_dict(
    result: Dict[str, Any],
    key: str,
    value: Any,
    default: Any = None,
) -> None:
    if value is None:
        if default is not None:
            result[key] = default
    else:
        result[key] = value


def normalize_strings(value: Any) -> Optional[List[str]]:
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        result = []
        for elem in iter(value):
            if isinstance(elem, str):
                result.append(elem)
            else:
                result.append(str(elem))
        return result
    return [str(value)]
