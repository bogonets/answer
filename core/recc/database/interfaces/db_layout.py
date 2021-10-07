# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.layout import Layout


class DbLayout(metaclass=ABCMeta):
    """
    Database layout interface.
    """

    @abstractmethod
    async def insert_layout(
        self,
        project_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_description_by_uid(
        self,
        uid: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_description_by_name(
        self,
        project_uid: int,
        name: str,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_extra_by_name(
        self,
        project_uid: int,
        name: str,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_layout_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_layout_by_name(self, project_uid: int, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_layout_by_uid(self, uid: int) -> Layout:
        raise NotImplementedError

    @abstractmethod
    async def select_layout_by_name(self, project_uid: int, name: str) -> Layout:
        raise NotImplementedError

    @abstractmethod
    async def select_layout_by_project_uid(self, project_uid: int) -> List[Layout]:
        raise NotImplementedError
