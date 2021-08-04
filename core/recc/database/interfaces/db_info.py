# -*- coding: utf-8 -*-

from typing import List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.info import Info


class DbInfo(metaclass=ABCMeta):
    """
    Database config(info) interface.
    """

    @abstractmethod
    async def create_info(
        self,
        key: str,
        value: str,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_info_value_by_key(
        self, key: str, value: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def upsert_info(
        self, key: str, value: str, created_or_updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_info_by_key(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_info_by_key(self, key: str) -> Info:
        raise NotImplementedError

    @abstractmethod
    async def get_infos(self) -> List[Info]:
        raise NotImplementedError

    @abstractmethod
    async def get_database_version(self) -> str:
        raise NotImplementedError