# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.project import Project


class ContextProject(ContextBase):
    async def create_project(
        self,
        group_uid: int,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.insert_project(
            group_uid=group_uid,
            slug=slug,
            name=name,
            description=description,
            features=features,
            extra=extra,
        )

    async def update_project(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_project_by_uid(
            uid=uid,
            name=name,
            description=description,
            features=features,
            extra=extra,
        )

    async def get_projects(
        self,
        group_uid: Optional[int] = None,
        remove_sensitive=True,
    ) -> List[Project]:
        if not group_uid:
            projects = await self.database.get_projects()
        else:
            projects = await self.database.get_project_by_group_uid(group_uid)
        if remove_sensitive:
            for project in projects:
                project.remove_sensitive()
        return projects

    async def get_project(self, uid: int, remove_sensitive=True) -> Project:
        project = await self.database.get_project_by_uid(uid)
        if remove_sensitive:
            project.remove_sensitive()
        return project

    async def delete_project(self, uid: int) -> None:
        await self.database.delete_project_by_uid(uid)
