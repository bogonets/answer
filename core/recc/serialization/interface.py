# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any

from recc.serialization.errors import (
    NotImplementedDeserializeError,
    NotImplementedSerializeError,
)


class SerializeInterface(metaclass=ABCMeta):
    @abstractmethod
    def __serialize__(self) -> Any:
        raise NotImplementedError


class DeserializeInterface(metaclass=ABCMeta):
    @abstractmethod
    def __deserialize__(self, data: Any) -> None:
        raise NotImplementedError


SERIALIZE_METHOD_NAME = SerializeInterface.__serialize__.__name__
DESERIALIZE_METHOD_NAME = DeserializeInterface.__deserialize__.__name__


class Serializable(SerializeInterface, DeserializeInterface):
    def __serialize__(self) -> Any:
        raise NotImplementedSerializeError()

    def __deserialize__(self, data: Any) -> None:
        raise NotImplementedDeserializeError()
