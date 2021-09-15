# -*- coding: utf-8 -*-

from typing import Optional, Any, List, Dict, Iterable
from abc import ABCMeta, abstractmethod


class DbUtils(metaclass=ABCMeta):
    """
    Database utils interface.
    """

    @abstractmethod
    async def execute_query(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def execute_queries(
        self,
        queries: Iterable[str],
        timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def fetch_rows(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_first_row(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_first_row_and_column(
        self,
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError
