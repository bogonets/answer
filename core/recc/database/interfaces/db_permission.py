# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.struct.permission import Permission


class DbPermission(metaclass=ABCMeta):
    """
    Database permission interface.
    """

    @abstractmethod
    async def create_permission(
        self,
        name: str,
        description: Optional[str] = None,
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
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_by_uid(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
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
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_description_by_name(
        self, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_extra_by_name(
        self, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_permission_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_permission_by_name(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_permission_by_uid(self, uid: int) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def get_permission_by_name(self, name: str) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def get_permissions(self) -> List[Permission]:
        raise NotImplementedError

    @abstractmethod
    async def get_project_permission_by_uid(
        self, user_uid: int, project_uid: int
    ) -> Permission:
        raise NotImplementedError
