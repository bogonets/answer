# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE
from recc.database.struct.project import Project
from recc.database.interfaces.db_project import DbProject
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.project import (
    INSERT_PROJECT,
    DELETE_PROJECT_BY_UID,
    SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG,
    SELECT_PROJECT_ALL,
    SELECT_PROJECT_BY_UID,
    SELECT_PROJECT_BY_GROUP_ID,
    SELECT_PROJECT_BY_BELOW_VISIBILITY,
    SELECT_PROJECT_COUNT,
    SELECT_PROJECT_BY_USER_UID,
    get_update_project_query_by_uid,
)


class PgProject(DbProject, PgBase):
    @overrides
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
        created = created_at if created_at else today()
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

    @overrides
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
        updated = updated_at if updated_at else today()
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

    @overrides
    async def delete_project_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_PROJECT_BY_UID, uid)

    @overrides
    async def select_project_uid_by_group_uid_and_slug(
        self, group_uid: int, slug: str
    ) -> int:
        return await self.column(
            int,
            SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG,
            group_uid,
            slug,
        )

    @overrides
    async def select_project_by_uid(self, uid: int) -> Project:
        return await self.row(Project, SELECT_PROJECT_BY_UID, uid)

    @overrides
    async def select_projects_by_group_uid(self, group_uid: int) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_BY_GROUP_ID, group_uid)

    @overrides
    async def select_projects_by_below_visibility(
        self, visibility: int
    ) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_BY_BELOW_VISIBILITY, visibility)

    @overrides
    async def select_projects(self) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_ALL)

    @overrides
    async def select_projects_count(self) -> int:
        return await self.column(int, SELECT_PROJECT_COUNT)

    @overrides
    async def select_projects_by_user_uid(self, user_uid: int) -> List[Project]:
        return await self.rows(Project, SELECT_PROJECT_BY_USER_UID, user_uid)
