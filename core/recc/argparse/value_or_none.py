# -*- coding: utf-8 -*-

from typing import List, Any, Union, Optional, Type, Mapping

ValueType = Optional[Union[str, int, float, bool]]
KeysType = Union[str, List[str]]
MapType = Mapping[str, Any]


def get_any_or_none(val: MapType, key: str) -> Optional[Any]:
    if key in val:
        return val[key]
    return None


def get_elem_or_none(
    obj: Optional[MapType],
    keys: KeysType,
    result_type: Type,
) -> Optional[Any]:
    if obj is None:
        return None
    if isinstance(keys, str):
        elem = get_any_or_none(obj, keys)
        if elem is None:
            return None
        try:
            return result_type(elem)
        except ValueError:
            return None
    elif isinstance(keys, list):
        keys_len = len(keys)
        if keys_len == 0:
            raise KeyError("Empty keys")
        elif keys_len == 1:
            return get_any_or_none(obj, keys[0])
        assert keys_len >= 2
        return get_elem_or_none(get_any_or_none(obj, keys[0]), keys[1:], result_type)
    return None


def get_str_or_none(obj: Optional[MapType], keys: KeysType) -> Optional[str]:
    return get_elem_or_none(obj, keys, str)


def get_int_or_none(obj: Optional[MapType], keys: KeysType) -> Optional[int]:
    return get_elem_or_none(obj, keys, int)


def get_float_or_none(obj: Optional[MapType], keys: KeysType) -> Optional[float]:
    return get_elem_or_none(obj, keys, float)


def get_bool_or_none(obj: Optional[MapType], keys: KeysType) -> Optional[bool]:
    return get_elem_or_none(obj, keys, bool)


def get_value_or_none(obj: Optional[MapType], keys: KeysType, cls: Type) -> ValueType:
    if cls == str:
        return get_str_or_none(obj, keys)
    elif cls == int:
        return get_int_or_none(obj, keys)
    elif cls == float:
        return get_float_or_none(obj, keys)
    elif cls == bool:
        return get_bool_or_none(obj, keys)
    else:
        raise KeyError(f"Unsupported type: {cls.__name__}.")
