# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.struct.group import Group


class DbGroup(metaclass=ABCMeta):
    """
    Database group interface.
    """

    @abstractmethod
    async def create_group(
        self,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_description_by_name(
        self, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_extra_by_name(
        self, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_by_name(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_group_by_uid(self, uid: int) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def get_group_by_name(self, name: str) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def get_groups(self) -> List[Group]:
        raise NotImplementedError
