# -*- coding: utf-8 -*-

from typing import Any, Optional, List
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
        name: str,
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
        created_at=datetime.now().astimezone(),
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_by_uid(
        self,
        uid: int,
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
        updated_at=datetime.now().astimezone(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_permission_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_uid_by_name(self, name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_name_by_uid(self, uid: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_by_uid(self, uid: int) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def select_permissions(self) -> List[Permission]:
        raise NotImplementedError

    @abstractmethod
    async def select_best_project_permission(
        self, user_uid: int, project_uid: int
    ) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def select_permission_by_user_uid_and_project_uid(
        self, user_uid: int, project_uid: int
    ) -> Permission:
        raise NotImplementedError
