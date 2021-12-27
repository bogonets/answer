# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional
from recc.rbac.rbac_subject import RbacSubject
from recc.rbac.rbac_role import RbacRole
from recc.rbac.rbac_permission import RbacPermission
from recc.rbac.rbac_exception import RbacKeyError, RbacMismatchContextError


class RbacDomain:
    def __init__(self, rbac, key: Any, parent: Optional["RbacDomain"] = None):
        self._rbac = rbac
        self._key = key
        self._parent = parent
        self._subdomains: Dict[Any, RbacDomain] = dict()
        self._subjects: Dict[RbacSubject, RbacRole] = dict()

    def __repr__(self) -> str:
        return f"RbacDomain[rbac={id(self._rbac)},key={self._key}]"

    def __str__(self) -> str:
        return self._key

    @property
    def context(self):
        return self._rbac

    def create_subdomain(self, key: Any) -> "RbacDomain":
        if key in self._subdomains:
            raise RbacKeyError(f"Already exists subdomain-key: {key}")
        project = RbacDomain(self._rbac, key, self)
        self._subdomains[key] = project
        return project

    def add_subject(self, subject: RbacSubject, role: RbacRole) -> None:
        if self.context != subject.context:
            raise RbacMismatchContextError
        if self.context != role.context:
            raise RbacMismatchContextError
        self._subjects[subject] = role

    def test_permission(
        self,
        subject: RbacSubject,
        *permission: RbacPermission,
        inherit=True,
    ) -> None:
        if self.context != subject.context:
            raise RbacMismatchContextError
        for p in permission:
            if self.context != p.context:
                raise RbacMismatchContextError

        if subject in self._subjects:
            role = self._subjects[subject]
            for p in permission:
                role.test_permission(p)
        elif inherit and self._parent is not None:
            self._parent.test_permission(subject, *permission, inherit=inherit)
        else:
            raise RbacKeyError(f"Not found subject: {str(subject)}")

    def has_permission(
        self,
        subject: RbacSubject,
        *permissions: RbacPermission,
        inherit=True,
    ) -> bool:
        try:
            self.test_permission(subject, *permissions, inherit=inherit)
        except:  # noqa
            return False
        else:
            return True
