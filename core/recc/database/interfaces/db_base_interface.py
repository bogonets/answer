# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Optional, Any, TypeVar, Type, List

RecordType = TypeVar("RecordType")
ColumnType = TypeVar("ColumnType")


class DbBaseInterface(metaclass=ABCMeta):
    """
    Database base interface.
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
    async def drop_database(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def execute(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def fetch_rows(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def fetch_first_row(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def fetch_first_row_column(
        self,
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def rows(
        self,
        cls: Type[RecordType],
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> List[RecordType]:
        raise NotImplementedError

    @abstractmethod
    async def row(
        self,
        cls: Type[RecordType],
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> RecordType:
        raise NotImplementedError

    @abstractmethod
    async def column(
        self,
        cls: Type[ColumnType],
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> ColumnType:
        raise NotImplementedError
