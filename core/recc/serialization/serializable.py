# -*- coding: utf-8 -*-

from typing import Any, List, Optional, Iterable, Dict, TypeVar, Final
from abc import ABCMeta, abstractmethod

_T = TypeVar("_T")

MAPPING_METHOD_ITEMS: Final[str] = "items"
MAPPING_METHOD_KEYS: Final[str] = "keys"
SEQUENCE_METHOD_INSERT: Final[str] = "insert"


class _Error(BaseException):
    def __init__(self, msg: str, key: Optional[str] = None):
        self.msg = msg
        self.key = key if key else str()

    def insert_first(self, key: Optional[str]) -> None:
        if not key:
            return
        if self.key:
            self.key = key + "." + self.key
        else:
            self.key = key


class SerializeError(_Error):
    def __init__(self, msg: str, key: Optional[str] = None):
        super().__init__(msg, key if key else "")


class DeserializeError(_Error):
    def __init__(self, msg: str, key: Optional[str] = None):
        super().__init__(msg, key if key else "")


class NotImplementedSerializeError(SerializeError):
    def __init__(self):
        super().__init__("Not implement serialize")


class NotImplementedDeserializeError(DeserializeError):
    def __init__(self):
        super().__init__("Not implement deserialize")


class SerializeInterface(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, version: int) -> Any:
        raise NotImplementedError


class DeserializeInterface(metaclass=ABCMeta):
    @abstractmethod
    def deserialize(self, version: int, data: Any) -> None:
        raise NotImplementedError


SERIALIZE_METHOD_NAME = SerializeInterface.serialize.__name__
DESERIALIZE_METHOD_NAME = DeserializeInterface.deserialize.__name__


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


class Serializable(SerializeInterface, DeserializeInterface):
    def serialize(self, version: int) -> Any:
        raise NotImplementedSerializeError()

    def deserialize(self, version: int, data: Any) -> None:
        raise NotImplementedDeserializeError()


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
