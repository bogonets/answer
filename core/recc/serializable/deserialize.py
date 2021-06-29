# -*- coding: utf-8 -*-

from inspect import isclass
from typing import (
    get_type_hints,
    get_origin,
    get_args,
    Union,
    Any,
    Tuple,
    TypeVar,
    Type,
    Iterable,
    Mapping,
    Optional,
    MutableSequence,
    MutableMapping,
)
from recc.exception.recc_error import ReccDeserializeError
from recc.serializable.serializable import (
    MAPPING_METHOD_ITEMS,
    MAPPING_METHOD_KEYS,
    SEQUENCE_METHOD_INSERT,
    DeserializeError,
    NotImplementedDeserializeError,
    DESERIALIZE_METHOD_NAME,
    is_deserialize_cls,
    is_serializable_pod_cls,
    is_none,
)
from recc.inspect.member import get_public_members

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")
_ET = TypeVar("_ET")
_MM = TypeVar("_MM", bound=MutableMapping)
_MS = TypeVar("_MS", bound=MutableSequence)
_FIRST_INDEX_KEY_STR = "0"
_ROOT_KEY = "<root>"


def _iterable_compatibility(data: Any) -> bool:
    assert not isinstance(data, bytes)
    assert not isinstance(data, bytearray)

    if isinstance(data, Mapping):
        return False
    elif isinstance(data, str):
        return False
    return isinstance(data, Iterable)


def _is_bytes(obj: Any) -> bool:
    if isinstance(obj, type):
        return issubclass(obj, bytes)
    else:
        return isinstance(obj, bytes)


def _is_bytearray(obj: Any) -> bool:
    if isinstance(obj, type):
        return issubclass(obj, bytearray)
    else:
        return isinstance(obj, bytearray)


def _deserialize_interface(version: int, data: Any, cls: Type[_T]) -> _T:
    result = cls()

    try:
        if hasattr(result, DESERIALIZE_METHOD_NAME):
            func = getattr(result, DESERIALIZE_METHOD_NAME)
            func(version, data)
            return result
    except (NotImplementedError, NotImplementedDeserializeError):
        pass

    result_hints = get_type_hints(cls)
    for key in result_hints.keys():
        serialize_value = getattr(data, key, None)
        hint = result_hints.get(key)
        origin = get_origin(hint)
        attr_cls = origin if origin else type(serialize_value)
        attr_value = _deserialize_any(version, serialize_value, attr_cls, key, hint)
        setattr(result, key, attr_value)
    return result


def _deserialize_mapping_by_keys(
    version: int,
    data: Any,
    cls: Type[_MM],
    keys: Iterable[str],
    elem_hint: Optional[Any] = None,
) -> _MM:
    assert issubclass(cls, MutableMapping)
    result = cls()
    for key in keys:
        serialize_value = getattr(data, key, None)
        attr_cls = elem_hint if elem_hint else type(serialize_value)
        attr_value = _deserialize_any(version, serialize_value, attr_cls, key)
        setattr(result, key, attr_value)
    return result


def _deserialize_mapping_by_items(
    version: int,
    cls: Type[_MM],
    items: Iterable[Tuple[str, _V]],
    elem_hint: Optional[Any] = None,
) -> _MM:
    assert issubclass(cls, MutableMapping)
    result = cls()
    for key, serialize_value in items:
        attr_cls = elem_hint if elem_hint else type(serialize_value)
        attr_value = _deserialize_any(version, serialize_value, attr_cls, key)
        result.setdefault(key, attr_value)
    return result


def _deserialize_mapping(
    version: int,
    data: Mapping,
    cls: Type[_MM],
    elem_hint: Optional[Any] = None,
) -> _MM:
    assert issubclass(cls, MutableMapping)

    if hasattr(data, MAPPING_METHOD_ITEMS):
        items_func = getattr(data, MAPPING_METHOD_ITEMS)
        items = items_func()
        return _deserialize_mapping_by_items(version, cls, items, elem_hint)
    elif hasattr(data, MAPPING_METHOD_KEYS):
        keys_func = getattr(data, MAPPING_METHOD_KEYS)
        keys = keys_func()
        return _deserialize_mapping_by_keys(version, data, cls, keys, elem_hint)
    else:
        members = get_public_members(data)
        return _deserialize_mapping_by_items(version, cls, members, elem_hint)


def _deserialize_mapping_any(
    version: int,
    data: Mapping,
    cls: Type[_MM],
    elem_hint: Optional[Any] = None,
) -> _MM:
    assert issubclass(cls, MutableMapping)
    if isinstance(data, Mapping):
        return _deserialize_mapping(version, data, cls, elem_hint)
    elif _iterable_compatibility(data):
        mapping = {str(i): v for i, v in enumerate(data)}
        return _deserialize_mapping(version, mapping, cls, elem_hint)
    else:
        mapping = {_FIRST_INDEX_KEY_STR: data}
        return _deserialize_mapping(version, mapping, cls, elem_hint)


def _deserialize_iterable(
    version: int,
    data: Iterable,
    cls: Type[_MS],
    elem_hint: Optional[Any] = None,
) -> _MS:
    assert issubclass(cls, MutableSequence)

    result = cls()
    if not hasattr(result, SEQUENCE_METHOD_INSERT):
        raise DeserializeError(f"Not found `{SEQUENCE_METHOD_INSERT}` method.")

    for i, serialize_value in enumerate(data):
        attr_cls = elem_hint if elem_hint else type(serialize_value)
        attr_value = _deserialize_any(version, serialize_value, attr_cls, f"[{i}]")
        result.insert(len(result), attr_value)
    return result


def _deserialize_iterable_any(
    version: int,
    data: Any,
    cls: Type[_MS],
    elem_hint: Optional[Any] = None,
) -> _MS:
    assert issubclass(cls, MutableSequence)
    if _iterable_compatibility(data):
        return _deserialize_iterable(version, data, cls, elem_hint)
    else:
        return _deserialize_iterable(version, [data], cls, elem_hint)


def _deserialize_object(version: int, data: Any, cls: Type[_T]) -> _T:
    result = cls()
    result_hints = get_type_hints(cls)
    for key, serialize_value in get_public_members(data):
        hint = result_hints.get(key)
        origin = get_origin(hint)

        if origin:
            attr_cls = origin
        elif hint:
            assert origin is None
            attr_cls = hint
        else:
            assert origin is None
            assert hint is None
            attr_cls = type(serialize_value)

        attr_value = _deserialize_any(version, serialize_value, attr_cls, key, hint)
        setattr(result, key, attr_value)
    return result


def _deserialize_any(
    version: int,
    data: Any,
    cls: Type[_T],
    key: Optional[str] = None,
    hint: Optional[Any] = None,
) -> Any:
    try:
        if data is None:
            return None

        type_origin = get_origin(hint)
        type_args = get_args(hint)
        assert isinstance(type_args, tuple)

        if type_origin is None:
            pass  # If there is no hint, it is deduced by the class.
        elif type_origin is Union:
            # Strip the Union hint.
            union_types = list(type_args)
            assert len(union_types) >= 2
            if type(None) in union_types:
                union_types.remove(type(None))
            if len(union_types) >= 2:
                raise DeserializeError("Two or more UNION types can not be deduced.")
            assert len(union_types) == 1
            return _deserialize_any(version, data, union_types[0], None, union_types[0])
        elif issubclass(type_origin, bytes):
            pass  # Does not support. check again with the class.
        elif issubclass(type_origin, bytearray):
            pass  # Does not support. check again with the class.
        elif is_deserialize_cls(type_origin):
            return _deserialize_interface(version, data, type_origin)
        elif is_serializable_pod_cls(type_origin):
            return type_origin(data)
        elif issubclass(type_origin, MutableMapping):
            elem_type = None
            if len(type_args) == 2:
                elem_type = type_args[1]
            return _deserialize_mapping_any(version, data, type_origin, elem_type)
        elif issubclass(type_origin, MutableSequence):
            elem_type = None
            if len(type_args) == 1:
                elem_type = type_args[0]
            return _deserialize_iterable_any(version, data, type_origin, elem_type)

        # Deduced by class.

        if not is_none(cls) and cls is not Any:
            if issubclass(cls, bytes):
                raise DeserializeError("The `bytes` type is not supported.")
            elif issubclass(cls, bytearray):
                raise DeserializeError("The `bytearray` type is not supported.")
            elif issubclass(cls, int):
                return int(data)
            elif issubclass(cls, float):
                return float(data)
            elif issubclass(cls, str):
                return str(data)
            elif is_deserialize_cls(cls):
                return _deserialize_interface(version, data, cls)
            elif issubclass(cls, MutableMapping):
                return _deserialize_mapping_any(version, data, cls)
            elif issubclass(cls, MutableSequence):
                return _deserialize_iterable_any(version, data, cls)
            elif isclass(cls):
                return _deserialize_object(version, data, cls)

        # Deduced by data.

        if isinstance(data, bytes):
            raise DeserializeError("The `bytes` data is not supported.")
        elif isinstance(data, bytearray):
            raise DeserializeError("The `bytearray` data is not supported.")
        elif isinstance(data, int):
            return int(data)
        elif isinstance(data, float):
            return float(data)
        elif isinstance(data, str):
            return str(data)
        elif isinstance(data, Mapping):
            return _deserialize_mapping(version, data, dict)
        elif isinstance(data, Iterable):
            return _deserialize_iterable(version, data, list)
        elif isclass(type(data)):
            return _deserialize_object(version, data, dict)

        raise DeserializeError(
            f"The data(`{type(data)}`) and class(`{cls}`) are not compatible."
        )
    except DeserializeError as e:
        e.insert_first(key)
        raise
    except BaseException as e:
        raise DeserializeError(str(e), key)


def deserialize(
    version: int,
    data: Any,
    cls: Type[_T],
    hint: Optional[Any] = None,
) -> _T:
    try:
        return _deserialize_any(version, data, cls, _ROOT_KEY, hint)
    except DeserializeError as e:
        raise ReccDeserializeError(f"Key(`{e.key}`) error: {e.msg}")
