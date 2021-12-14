# -*- coding: utf-8 -*-

from typing import Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.info import Info


class DbInfo(metaclass=ABCMeta):
    """
    Database config(info) interface.
    """

    @abstractmethod
    async def insert_info(
        self,
        key: str,
        value: str,
        created_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_info_value_by_key(
        self,
        key: str,
        value: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def upsert_info(
        self,
        key: str,
        value: str,
        created_or_updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_info_by_key(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists_info_by_key(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def select_info_by_key(self, key: str) -> Info:
        raise NotImplementedError

    @abstractmethod
    async def select_infos_like(self, like: str) -> List[Info]:
        raise NotImplementedError

    @abstractmethod
    async def select_infos(self) -> List[Info]:
        raise NotImplementedError

    @abstractmethod
    async def select_database_version(self) -> str:
        raise NotImplementedError
