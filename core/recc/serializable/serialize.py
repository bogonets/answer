# -*- coding: utf-8 -*-

from typing import (
    Dict,
    Any,
    List,
    Tuple,
    TypeVar,
    Iterable,
    Mapping,
    Optional,
)
from recc.exception.recc_error import ReccSerializeError
from recc.serializable.serializable import (
    MAPPING_METHOD_ITEMS,
    MAPPING_METHOD_KEYS,
    SerializeError,
    NotImplementedSerializeError,
    SERIALIZE_METHOD_NAME,
    is_serialize_obj,
    is_serializable_pod_obj,
)
from recc.inspect.member import get_public_members

_K = TypeVar("_K")
_V = TypeVar("_V")


def _create_serialize_dict(
    version: int, items: Iterable[Tuple[str, Any]]
) -> Dict[str, Any]:
    result: Dict[str, Any] = dict()
    for key, val in items:
        assert isinstance(key, str)
        if val is None:
            continue
        serialize_value = _serialize_any(version, val, key)
        if serialize_value is None:
            continue
        result[key] = serialize_value
    return result


def _serialize_interface(version: int, obj: Any) -> Dict[str, Any]:
    try:
        if hasattr(obj, SERIALIZE_METHOD_NAME):
            serialize_func = getattr(obj, SERIALIZE_METHOD_NAME)
            return serialize_func(version)
    except (NotImplementedError, NotImplementedSerializeError):
        pass
    return _create_serialize_dict(version, get_public_members(obj))


def _serialize_mapping(version: int, obj: Mapping) -> Dict[str, Any]:
    items: List[Tuple[str, Any]]
    if hasattr(obj, MAPPING_METHOD_ITEMS):
        items_func = getattr(obj, MAPPING_METHOD_ITEMS)
        items = items_func()
    elif hasattr(obj, MAPPING_METHOD_KEYS):
        keys_func = getattr(obj, MAPPING_METHOD_KEYS)
        items = [(str(k), getattr(obj, str(k))) for k in keys_func()]
    else:
        items = get_public_members(obj)
    return _create_serialize_dict(version, items)


def _serialize_iterable(version: int, obj: Iterable) -> List[Any]:
    result: List[Any] = list()
    for i, item in enumerate(obj):
        serialize_value = _serialize_any(version, item, f"[{i}]")
        if serialize_value is None:
            continue
        result.append(serialize_value)
    return result


def _serialize_common(version: int, obj: Any) -> Dict[str, Any]:
    return _create_serialize_dict(version, get_public_members(obj))


def _serialize_any(version: int, obj: Any, key: Optional[str] = None) -> Any:
    try:
        if obj is None:
            return None
        elif is_serialize_obj(obj):
            return _serialize_interface(version, obj)
        elif is_serializable_pod_obj(obj):
            return obj
        elif isinstance(obj, Mapping):
            return _serialize_mapping(version, obj)
        elif isinstance(obj, Iterable):
            return _serialize_iterable(version, obj)
        else:
            return _serialize_common(version, obj)
    except SerializeError as e:
        e.insert_first(key)
        raise
    except BaseException as e:
        raise SerializeError(str(e), key)


def serialize(version: int, obj: Any) -> Dict[str, Any]:
    try:
        return _serialize_any(version, obj)
    except SerializeError as e:
        raise ReccSerializeError(f"Key({e.key}) error: {e.msg}")
