# -*- coding: utf-8 -*-

from typing import Dict, Any
from recc.rbac.rbac_domain import RbacDomain
from recc.rbac.rbac_permission import RbacPermission
from recc.rbac.rbac_role import RbacRole
from recc.rbac.rbac_subject import RbacSubject
from recc.rbac.rbac_exception import RbacKeyError


class Rbac:
    def __init__(self):
        self._domains: Dict[Any, RbacDomain] = dict()
        self._roles: Dict[Any, RbacRole] = dict()
        self._permissions: Dict[Any, RbacPermission] = dict()
        self._subjects: Dict[Any, RbacSubject] = dict()

    def create_domain(self, key: Any) -> RbacDomain:
        if key in self._domains:
            raise RbacKeyError(f"Already exists domain-key: {key}")
        domain = RbacDomain(self, key)
        self._domains[key] = domain
        return domain

    def create_role(self, key: Any) -> RbacRole:
        if key in self._roles:
            raise RbacKeyError(f"Already exists role-key: {key}")
        role = RbacRole(self, key)
        self._roles[key] = role
        return role

    def create_permission(self, key: Any) -> RbacPermission:
        if key in self._permissions:
            raise RbacKeyError(f"Already exists permission-key: {key}")
        perm = RbacPermission(self, key)
        self._permissions[key] = perm
        return perm

    def create_subject(self, key: Any) -> RbacSubject:
        if key in self._subjects:
            raise RbacKeyError(f"Already exists subject-key: {key}")
        subject = RbacSubject(self, key)
        self._subjects[key] = subject
        return subject
