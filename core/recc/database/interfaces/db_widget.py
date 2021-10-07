# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.widget import Widget


class DbWidget(metaclass=ABCMeta):
    """
    Database widget interface.
    """

    @abstractmethod
    async def insert_widget(
        self,
        layout_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_description_by_uid(
        self,
        uid: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_description_by_name(
        self,
        layout_uid: int,
        name: str,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_extra_by_name(
        self,
        layout_uid: int,
        name: str,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_widget_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_widget_by_name(self, layout_uid: int, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_widget_by_uid(self, uid: int) -> Widget:
        raise NotImplementedError

    @abstractmethod
    async def select_widget_by_name(self, layout_uid: int, name: str) -> Widget:
        raise NotImplementedError

    @abstractmethod
    async def select_widget_by_layout_uid(self, layout_uid: int) -> List[Widget]:
        raise NotImplementedError
