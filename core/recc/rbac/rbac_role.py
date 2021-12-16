# -*- coding: utf-8 -*-

from typing import Set, Any
from recc.rbac.rbac_permission import RbacPermission
from recc.rbac.rbac_exception import RbacMismatchContextError, RbacPermissionError


class RbacRole:
    def __init__(self, rbac, key: Any):
        self._rbac = rbac
        self._key = key
        self._allows: Set[RbacPermission] = set()
        self._denies: Set[RbacPermission] = set()

    def __repr__(self) -> str:
        return f"RbacRole[rbac={id(self._rbac)},key={self._key}]"

    def __str__(self) -> str:
        return self._key

    @property
    def context(self):
        return self._rbac

    @property
    def key(self) -> Any:
        return self._key

    def allow_permission(self, *permissions: RbacPermission) -> None:
        for p in permissions:
            if self.context != p.context:
                raise RbacMismatchContextError

        for p in permissions:
            self._allows.add(p)

    def deny_permission(self, *permissions: RbacPermission) -> None:
        for p in permissions:
            if self.context != p.context:
                raise RbacMismatchContextError

        for p in permissions:
            self._denies.add(p)

    def test_allow_permission(self, permission: RbacPermission) -> None:
        if self.context != permission.context:
            raise RbacMismatchContextError

        if permission not in self._allows:
            raise RbacPermissionError(f"Not allowed permission: {str(permission)}")

    def test_deny_permission(self, permission: RbacPermission) -> None:
        if self.context != permission.context:
            raise RbacMismatchContextError

        if permission in self._denies:
            raise RbacPermissionError(f"Denied permission: {str(permission)}")

    def test_permission(self, permission: RbacPermission) -> None:
        if self.context != permission.context:
            raise RbacMismatchContextError

        self.test_allow_permission(permission)
        self.test_deny_permission(permission)
