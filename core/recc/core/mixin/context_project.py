# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.project import Project
from recc.database.struct.project_member import ProjectMember
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE, VISIBILITY_LEVEL_INTERNAL


class ContextProject(ContextBase):
    async def create_project(
        self,
        group_uid: int,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility=VISIBILITY_LEVEL_PRIVATE,
        extra: Optional[Any] = None,
        owner_uid: Optional[int] = None,
    ) -> int:
        project_uid = await self.database.insert_project(
            group_uid=group_uid,
            slug=slug,
            name=name,
            description=description,
            features=features,
            visibility=visibility,
            extra=extra,
        )
        if owner_uid is not None:
            owner_permission_uid = self.database.get_owner_permission_uid()
            await self.database.insert_project_member(
                project_uid, owner_uid, owner_permission_uid
            )
        group_slug = await self.get_group_slug(group_uid)
        await self.plugins.create_project(group_slug, slug)
        return project_uid

    async def update_project(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility: Optional[int] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_project_by_uid(
            uid=uid,
            name=name,
            description=description,
            features=features,
            visibility=visibility,
            extra=extra,
        )

    async def delete_project(self, uid: int) -> None:
        project = await self.database.select_project_by_uid(uid)
        group_slug = await self.get_group_slug(project.group_uid)
        await self.plugins.delete_project(group_slug, project.slug)

        await self.database.delete_project_by_uid(uid)

    async def get_projects(self, group_uid: Optional[int] = None) -> List[Project]:
        if not group_uid:
            return await self.database.select_projects()
        else:
            return await self.database.select_projects_by_group_uid(group_uid)

    async def get_project(self, uid: int) -> Project:
        return await self.database.select_project_by_uid(uid)

    async def get_projects_for_accessible(self) -> List[Project]:
        return await self.database.select_projects_by_below_visibility(
            VISIBILITY_LEVEL_INTERNAL
        )

    async def get_projects_by_user(self, user_uid: int) -> List[Project]:
        return await self.database.select_projects_by_user_uid(user_uid)

    async def get_project_members(self, project_uid: int) -> List[ProjectMember]:
        return await self.database.select_project_members_by_project_uid(project_uid)

    async def get_project_member(
        self, project_uid: int, user_uid: int
    ) -> ProjectMember:
        return await self.database.select_project_member(project_uid, user_uid)

    async def add_project_member(
        self, project_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        return await self.database.insert_project_member(
            project_uid=project_uid,
            user_uid=user_uid,
            permission_uid=permission_uid,
        )

    async def update_project_member(
        self, project_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        return await self.database.update_project_member_permission(
            project_uid=project_uid,
            user_uid=user_uid,
            permission_uid=permission_uid,
        )

    async def remove_project_member(self, project_uid: int, user_uid: int) -> None:
        await self.database.delete_project_member(project_uid, user_uid)
