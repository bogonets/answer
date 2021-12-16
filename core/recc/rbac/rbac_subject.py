# -*- coding: utf-8 -*-

from typing import Any


class RbacSubject:
    def __init__(self, rbac, key: Any):
        self._rbac = rbac
        self._key = key

    def __repr__(self) -> str:
        return f"RbacSubject[rbac={id(self._rbac)},key={self._key}]"

    def __str__(self) -> str:
        return self._key

    @property
    def context(self):
        return self._rbac

    @property
    def key(self) -> Any:
        return self._key
