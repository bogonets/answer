# -*- coding: utf-8 -*-

from typing import Optional, List, Any
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.permission import Permission


class DbPermission(metaclass=ABCMeta):
    """
    Database permission interface.
    """

    @abstractmethod
    async def insert_permission(
        self,
        slug: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_permission(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_uid_by_slug(self, slug: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_slug_by_uid(self, uid: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_by_slug(self, slug: str) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_by_uid(self, uid: int) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_all(self) -> List[Permission]:
        raise NotImplementedError
