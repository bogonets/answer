# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class DbMisc(metaclass=ABCMeta):
    """
    Database miscellaneous interface.
    """

    @abstractmethod
    async def create_tables(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def drop_tables(self) -> None:
        raise NotImplementedError
