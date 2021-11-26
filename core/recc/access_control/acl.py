# -*- coding: utf-8 -*-

from typing import Any, List, Optional
from aiohttp.web_exceptions import HTTPBadRequest, HTTPForbidden
from recc.access_control.policy import Policy, test_policies
from recc.core.context import Context
from recc.session.session_ex import SessionEx
from recc.conversion.string import object_to_strings
from recc.variables.annotation import (
    ANNOTATION_GROUP_PERMISSIONS,
    ANNOTATION_PROJECT_PERMISSIONS,
    ANNOTATION_FEATURE_PERMISSIONS,
    ANNOTATION_ADMIN_PERMISSION,
)


def _object_to_policies(obj: Any) -> List[Policy]:
    if isinstance(obj, Policy):
        return [obj]
    elif isinstance(obj, int):
        return [Policy(obj)]
    elif isinstance(obj, str):
        return [Policy[obj]]
    elif isinstance(obj, set) or isinstance(obj, list):
        result = list()
        for oo in obj:
            for o in _object_to_policies(oo):
                result.append(o)
        return result
    else:
        raise RuntimeError(f"Unsupported Policy type: {type(obj).__name__}")


class AccessControlList:

    groups: List[Policy]
    projects: List[Policy]
    features: List[str]
    admin: bool

    def __init__(
        self,
        func,
        group_policies: Optional[List[Policy]] = None,
        project_policies: Optional[List[Policy]] = None,
        has_features: Optional[List[str]] = None,
        has_admin=False,
    ):
        self.groups = list()
        self.projects = list()
        self.features = list()

        if group_policies:
            for policy in group_policies:
                self.groups.append(policy)
        annotation_group = getattr(func, ANNOTATION_GROUP_PERMISSIONS, None)
        if annotation_group:
            for policy in _object_to_policies(annotation_group):
                self.groups.append(policy)

        if project_policies:
            for policy in project_policies:
                self.projects.append(policy)
        annotation_project = getattr(func, ANNOTATION_PROJECT_PERMISSIONS, None)
        if annotation_project:
            for policy in _object_to_policies(annotation_project):
                self.projects.append(policy)

        if has_features:
            for feature in has_features:
                self.features.append(feature)
        annotation_feature = getattr(func, ANNOTATION_FEATURE_PERMISSIONS, None)
        if annotation_feature:
            for feature in object_to_strings(annotation_feature):
                self.features.append(feature)

        annotation_admin = getattr(func, ANNOTATION_ADMIN_PERMISSION, False)
        self.admin = True if (has_admin or annotation_admin) else False

    def exists(self) -> bool:
        if self.groups:
            return True
        if self.projects:
            return True
        return self.admin

    def test_features(self, users_features: List[str]) -> None:
        for feature in self.features:
            if feature not in users_features:
                raise PermissionError(f"{feature} feature does not exist.")

    async def test_groups(
        self,
        context: Context,
        session: SessionEx,
        group_name: Optional[str],
    ) -> None:
        if not group_name:
            raise HTTPBadRequest(reason="The group name is missing")

        try:
            permission = await context.get_group_raw_permission(session, group_name)
            if Policy.HasFeatures in self.groups:
                self.test_features(permission.features)
            test_policies(self.groups, permission)
        except PermissionError as e:
            raise HTTPForbidden(reason=str(e))

    async def test_projects(
        self,
        context: Context,
        session: SessionEx,
        group_name: Optional[str],
        project_name: Optional[str],
    ) -> None:
        if not group_name:
            raise HTTPBadRequest(reason="The group name is missing")
        if not project_name:
            raise HTTPBadRequest(reason="The project name is missing")

        try:
            permission = await context.get_project_raw_permission(
                session, group_name, project_name
            )
            if Policy.HasFeatures in self.projects:
                self.test_features(permission.features)
            test_policies(self.projects, permission)
        except PermissionError as e:
            raise HTTPForbidden(reason=str(e))
