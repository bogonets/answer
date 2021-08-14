# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.group import Group


class DbGroup(metaclass=ABCMeta):
    """
    Database group interface.
    """

    @abstractmethod
    async def create_group(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_slug_by_uid(
        self, uid: int, slug: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_description_by_slug(
        self, slug: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_extra_by_slug(
        self, slug: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_features_by_uid(
        self, uid: int, features: List[str], updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_features_by_slug(
        self, slug: str, features: List[str], updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_by_slug(self, slug: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_group_uid_by_slug(self, slug: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_group_by_uid(self, uid: int) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def get_group_by_slug(self, slug: str) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def get_groups(self) -> List[Group]:
        raise NotImplementedError

    @abstractmethod
    async def get_groups_count(self) -> int:
        raise NotImplementedError
