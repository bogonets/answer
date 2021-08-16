# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.project import Project


class ContextProject(ContextBase):
    async def create_project(
        self,
        group: str,
        project: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        group_uid = await self.database.get_group_uid_by_slug(group)
        assert group_uid is not None
        await self.database.create_project(
            group_uid=group_uid,
            slug=project,
            name=name,
            description=description,
            features=features,
            extra=extra,
        )

    async def get_projects(
        self,
        group: Optional[str] = None,
        remove_sensitive=True,
    ) -> List[Project]:
        if not group:
            projects = await self.database.get_projects()
        else:
            projects = await self.database.get_project_by_group_slug(group)
        if remove_sensitive:
            for project in projects:
                project.remove_sensitive()
        return projects

    async def get_project_uid(
        self, group_uid: int, project_slug: str, caching=True
    ) -> int:
        if not project_slug:
            raise ValueError("The `project_slug` argument is empty.")
        uid = self.cache.get_project_uid(group_uid, project_slug)
        if uid is None:
            uid = await self.database.get_project_uid_by_group_uid_and_slug(
                group_uid, project_slug
            )
            if caching:
                self.cache.set_project(uid, group_uid, project_slug)
        return uid

    async def get_project(self, project_uid: int, remove_sensitive=True) -> Project:
        project = await self.database.get_project_by_uid(project_uid)
        if remove_sensitive:
            project.remove_sensitive()
        return project

    async def get_project_by_fullpath(self, group: str, project: str) -> Project:
        group_uid = await self.database.get_group_uid_by_slug(group)
        assert group_uid is not None
        return await self.database.get_project_by_slug(group_uid, project)

    async def update_project(
        self,
        project_uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_project_by_uid(
            uid=project_uid,
            name=name,
            description=description,
            features=features,
            extra=extra,
        )

    async def delete_project(self, project_uid: int) -> None:
        await self.database.delete_project_by_uid(project_uid)

    async def delete_project_by_fullpath(self, group: str, project: str) -> None:
        project_uid = await self.database.get_project_uid_by_fullpath(group, project)
        assert project_uid is not None
        await self.database.delete_project_by_uid(project_uid)
