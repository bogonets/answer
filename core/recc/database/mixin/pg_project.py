# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.project import (
    DELETE_PROJECT_BY_UID,
    INSERT_PROJECT,
    SELECT_PROJECT_ALL,
    SELECT_PROJECT_BY_BELOW_VISIBILITY,
    SELECT_PROJECT_BY_GROUP_ID,
    SELECT_PROJECT_BY_UID,
    SELECT_PROJECT_BY_USER_UID,
    SELECT_PROJECT_COUNT,
    SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG,
    get_update_project_query_by_uid,
)
from recc.packet.project import Project
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


class PgProject(PgBase):
    async def insert_project(
        self,
        group_uid: int,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility=VISIBILITY_LEVEL_PRIVATE,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else tznow()
        return await self.column(
            int,
            INSERT_PROJECT,
            group_uid,
            slug,
            name,
            description,
            features,
            visibility,
            extra,
            created,
        )

    async def update_project_by_uid(
        self,
        uid: Optional[int] = None,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility: Optional[int] = None,
        extra: Optional[Any] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        query, args = get_update_project_query_by_uid(
            uid=uid,
            slug=slug,
            name=name,
            description=description,
            features=features,
            visibility=visibility,
            extra=extra,
            updated_at=updated,
        )
        await self.execute(query, *args)

    async def delete_project_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_PROJECT_BY_UID, uid)

    async def select_project_uid_by_group_uid_and_slug(
        self, group_uid: int, slug: str
    ) -> int:
        return await self.column(
            int,
            SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG,
            group_uid,
            slug,
        )

    async def select_project_by_uid(self, uid: int) -> Project:
        return await self.row(Project, SELECT_PROJECT_BY_UID, uid)

    async def select_projects_by_group_uid(self, group_uid: int) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_BY_GROUP_ID, group_uid)

    async def select_projects_by_below_visibility(
        self, visibility: int
    ) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_BY_BELOW_VISIBILITY, visibility)

    async def select_projects(self) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_ALL)

    async def select_projects_count(self) -> int:
        return await self.column(int, SELECT_PROJECT_COUNT)

    async def select_projects_by_user_uid(self, user_uid: int) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_BY_USER_UID, user_uid)
