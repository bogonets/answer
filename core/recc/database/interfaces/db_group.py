# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.group import Group
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


class DbGroup(metaclass=ABCMeta):
    """
    Database group interface.
    """

    @abstractmethod
    async def insert_group(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility=VISIBILITY_LEVEL_PRIVATE,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_group_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility: Optional[int] = None,
        extra: Optional[Any] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_group_uid_by_slug(self, slug: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_group_slug_by_uid(self, uid: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def select_group_by_uid(self, uid: int) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def select_groups_by_below_visibility(self, visibility: int) -> List[Group]:
        raise NotImplementedError

    @abstractmethod
    async def select_groups(self) -> List[Group]:
        raise NotImplementedError

    @abstractmethod
    async def select_groups_count(self) -> int:
        raise NotImplementedError
