# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, Union

ValueType = Union[bytes, memoryview, str, int, float]


class CacheStoreInterface(metaclass=ABCMeta):
    """
    Cache Store interface.
    """

    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, val: ValueType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def mset(self, pairs: Dict[str, ValueType]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        raise NotImplementedError

    @abstractmethod
    async def append(self, key: str, val: ValueType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def expire(self, key: str, seconds: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *keys: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, *keys: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        raise NotImplementedError
