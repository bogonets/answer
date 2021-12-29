# -*- coding: utf-8 -*-

from typing import List
from abc import ABCMeta, abstractmethod
from recc.database.struct.role_permission import RolePermission


class DbRolePermission(metaclass=ABCMeta):
    """
    Database role-permission interface.
    """

    @abstractmethod
    async def insert_role_permission(self, role_uid: int, permission_uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert_role_permissions_by_slug(
        self, role_uid: int, permission_slugs: List[str]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_role_permission(self, role_uid: int, permission_uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_role_permissions_by_slug(
        self, role_uid: int, permission_slugs: List[str]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_role_permission_all(self) -> List[RolePermission]:
        raise NotImplementedError

    @abstractmethod
    async def select_role_permission_by_role_uid(
        self, role_uid: int
    ) -> List[RolePermission]:
        raise NotImplementedError
