# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


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
    async def set(self, key: str, val: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def append(self, key: str, val: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def expire(self, key: str, seconds: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: str) -> bool:
        raise NotImplementedError
