# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional

from recc.packet.user import UserInfo


class DbUserInfo(metaclass=ABCMeta):
    """
    Database user's extra information interface.
    """

    @abstractmethod
    async def insert_user_info(
        self,
        user_uid: int,
        key: str,
        value: str,
        created_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_info_value_by_key(
        self,
        user_uid: int,
        key: str,
        value: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def upsert_user_info(
        self,
        user_uid: int,
        key: str,
        value: str,
        created_or_updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_info_by_key(self, user_uid: int, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists_user_info_by_key(self, user_uid: int, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def select_user_info_by_key(self, user_uid: int, key: str) -> UserInfo:
        raise NotImplementedError

    @abstractmethod
    async def select_user_infos_like(self, user_uid: int, like: str) -> List[UserInfo]:
        raise NotImplementedError

    @abstractmethod
    async def select_user_infos(self, user_uid: int) -> List[UserInfo]:
        raise NotImplementedError
