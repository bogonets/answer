# -*- coding: utf-8 -*-

from enum import Enum
from abc import ABCMeta, abstractmethod


class PluginCategory(Enum):
    UNKNOWN = 0
    LAMBDA = 1
    WIDGET = 2


class PluginInstallType(Enum):
    UNKNOWN = 0
    LOCAL = 1
    GIT = 2


class SlotDirection(Enum):
    UNKNOWN = 0
    INPUT = 1
    OUTPUT = 2


class DbOpen(metaclass=ABCMeta):
    """
    Database open interface.
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
    async def drop(self) -> None:
        raise NotImplementedError
