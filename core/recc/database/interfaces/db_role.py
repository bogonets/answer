# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.role import Role


class DbRole(metaclass=ABCMeta):
    """
    Database role interface.
    """

    @abstractmethod
    async def insert_role(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout=False,
        w_layout=False,
        r_storage=False,
        w_storage=False,
        r_manager=False,
        w_manager=False,
        r_graph=False,
        w_graph=False,
        r_member=False,
        w_member=False,
        r_setting=False,
        w_setting=False,
        hidden=False,
        lock=False,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_role_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout: Optional[bool] = None,
        w_layout: Optional[bool] = None,
        r_storage: Optional[bool] = None,
        w_storage: Optional[bool] = None,
        r_manager: Optional[bool] = None,
        w_manager: Optional[bool] = None,
        r_graph: Optional[bool] = None,
        w_graph: Optional[bool] = None,
        r_member: Optional[bool] = None,
        w_member: Optional[bool] = None,
        r_setting: Optional[bool] = None,
        w_setting: Optional[bool] = None,
        hidden: Optional[bool] = None,
        lock: Optional[bool] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_role_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_role_uid_by_slug(self, slug: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_role_slug_by_uid(self, uid: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def select_role_by_uid(self, uid: int) -> Role:
        raise NotImplementedError

    @abstractmethod
    async def select_role_lock_by_uid(self, uid: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def select_role_all(self) -> List[Role]:
        raise NotImplementedError

    @abstractmethod
    async def select_role_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> Role:
        raise NotImplementedError

    @abstractmethod
    async def select_role_by_user_uid_and_project_uid(
        self, user_uid: int, project_uid: int
    ) -> Role:
        raise NotImplementedError
