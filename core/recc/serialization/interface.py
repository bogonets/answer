# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any
from recc.serialization.errors import (
    NotImplementedSerializeError,
    NotImplementedDeserializeError,
)


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


class Serializable(SerializeInterface, DeserializeInterface):
    def serialize(self, version: int) -> Any:
        raise NotImplementedSerializeError()

    def deserialize(self, version: int, data: Any) -> None:
        raise NotImplementedDeserializeError()
