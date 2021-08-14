# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.project import Project


class ContextProject(ContextBase):
    async def create_project(self, group_name: str, project_name: str) -> None:
        group = await self.database.get_group_by_slug(group_name)
        assert group.uid is not None
        await self.database.create_project(group.uid, project_name)

    async def get_projects(self, group_name: str) -> List[Project]:
        group = await self.database.get_group_by_slug(group_name)
        assert group.uid is not None
        return await self.database.get_project_by_group_uid(group.uid)

    async def get_project(self, group_name: str, project_name: str) -> Project:
        group = await self.database.get_group_by_slug(group_name)
        assert group.uid is not None
        return await self.database.get_project_by_name(group.uid, project_name)

    async def update_project(
        self,
        group_name: str,
        project_name: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        group = await self.database.get_group_by_slug(group_name)
        project = await self.database.get_project_by_name(group.uid, project_name)
        assert group.uid is not None
        assert project.uid is not None
        await self.database.update_project_by_uid(
            project.uid,
            name=name,
            description=description,
            features=features,
            extra=extra,
        )

    async def delete_project(self, group_name: str, project_name: str) -> None:
        group = await self.database.get_group_by_slug(group_name)
        project = await self.database.get_project_by_name(group.uid, project_name)
        assert group.uid is not None
        assert project.uid is not None
        await self.database.delete_project_by_uid(project.uid)
