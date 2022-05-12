# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Optional


class ContainerOpen(metaclass=ABCMeta):
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
    async def version(self, key: Optional[str] = None) -> str:
        raise NotImplementedError
