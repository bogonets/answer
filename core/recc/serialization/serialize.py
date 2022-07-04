# -*- coding: utf-8 -*-

from datetime import date, datetime, time
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from numpy import ndarray

from recc.inspect.member import get_public_instance_attributes
from recc.serialization.errors import NotImplementedSerializeError, SerializeError
from recc.serialization.interface import SERIALIZE_METHOD_NAME
from recc.serialization.numpy import numpy_serialize
from recc.serialization.utils import (
    MAPPING_METHOD_ITEMS,
    MAPPING_METHOD_KEYS,
    is_serializable_pod_obj,
    is_serialize_obj,
)


def _create_serialize_dict(items: Iterable[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = dict()
    for key, val in items:
        assert isinstance(key, str)
        if val is None:
            continue
        serialize_value = _serialize_any(val, key)
        if serialize_value is None:
            continue
        result[key] = serialize_value
    return result


def _serialize_interface(obj: Any) -> Dict[str, Any]:
    try:
        if hasattr(obj, SERIALIZE_METHOD_NAME):
            serialize_func = getattr(obj, SERIALIZE_METHOD_NAME)
            return serialize_func()
    except (NotImplementedError, NotImplementedSerializeError):
        pass
    return _create_serialize_dict(get_public_instance_attributes(obj))


def _serialize_mapping(obj: Mapping) -> Dict[str, Any]:
    items: List[Tuple[str, Any]]
    if hasattr(obj, MAPPING_METHOD_ITEMS):
        items_func = getattr(obj, MAPPING_METHOD_ITEMS)
        items = items_func()
    elif hasattr(obj, MAPPING_METHOD_KEYS):
        keys_func = getattr(obj, MAPPING_METHOD_KEYS)
        items = [(str(k), getattr(obj, str(k))) for k in keys_func()]
    else:
        items = get_public_instance_attributes(obj)
    return _create_serialize_dict(items)


def _serialize_iterable(obj: Iterable) -> List[Any]:
    result: List[Any] = list()
    for i, item in enumerate(obj):
        serialize_value = _serialize_any(item, f"[{i}]")
        if serialize_value is None:
            continue
        result.append(serialize_value)
    return result


def _serialize_common(obj: Any) -> Dict[str, Any]:
    return _create_serialize_dict(get_public_instance_attributes(obj))


def _serialize_any(obj: Any, key: Optional[str] = None) -> Any:
    try:
        if obj is None:
            return None
        elif isinstance(obj, (bytes, bytearray)):
            return obj
        elif isinstance(obj, memoryview):
            return obj.tobytes()
        elif isinstance(obj, ndarray):
            return numpy_serialize(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        elif is_serialize_obj(obj):
            return _serialize_interface(obj)
        elif is_serializable_pod_obj(obj):
            return obj
        elif isinstance(obj, Mapping):
            return _serialize_mapping(obj)
        elif isinstance(obj, Iterable):
            return _serialize_iterable(obj)
        else:
            return _serialize_common(obj)
    except SerializeError as e:
        e.insert_first(key)
        raise
    except BaseException as e:
        raise SerializeError(str(e), key)


def serialize(obj: Any) -> Any:
    try:
        return _serialize_any(obj)
    except SerializeError as e:
        raise KeyError(f"Key({e.key}) error: {e.msg}")


def serialize_default(obj: Any) -> Any:
    return serialize(obj)
