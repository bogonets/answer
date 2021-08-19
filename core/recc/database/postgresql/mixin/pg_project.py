# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.project import Project
from recc.database.interfaces.db_project import DbProject
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.project import (
    INSERT_PROJECT,
    DELETE_PROJECT_BY_UID,
    SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG,
    SELECT_PROJECT_ALL,
    SELECT_PROJECT_BY_UID,
    SELECT_PROJECT_BY_GROUP_ID,
    SELECT_PROJECT_COUNT,
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
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> int:
        query = INSERT_PROJECT
        uid = await self.fetch_val(
            query,
            group_uid,
            slug,
            name,
            description,
            features,
            extra,
            created_at,
        )
        params_msg = f"group_uid={group_uid},slug={slug}"
        logger.info(f"insert_project({params_msg}) -> {uid}")
        return uid

    @overrides
    async def update_project_by_uid(
        self,
        uid: Optional[int] = None,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        query, args = get_update_project_query_by_uid(
            uid=uid,
            slug=slug,
            name=name,
            description=description,
            features=features,
            extra=extra,
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        params_msg = f"uid={uid}"
        logger.info(f"update_project_by_uid({params_msg}) ok.")

    @overrides
    async def delete_project_by_uid(self, uid: int) -> None:
        query = DELETE_PROJECT_BY_UID
        await self.execute(query, uid)
        logger.info(f"delete_project_by_uid(uid={uid}) ok.")

    @overrides
    async def select_project_uid_by_group_uid_and_slug(
        self, group_uid: int, slug: str
    ) -> int:
        query = SELECT_PROJECT_UID_BY_GROUP_UID_AND_SLUG
        row = await self.fetch_row(query, group_uid, slug)
        params_msg = f"group_uid={group_uid},slug={slug}"
        if not row:
            raise RuntimeError(f"Not found project: {params_msg}")
        result = row.get("uid")
        if result is None:
            raise RuntimeError(f"Not found project: {params_msg}")
        msg = f"select_project_uid_by_group_uid_and_slug({params_msg}) -> {result}"
        logger.info(msg)
        return result

    @overrides
    async def select_projects(self) -> List[Project]:
        result: List[Project] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PROJECT_ALL
                async for row in conn.cursor(query):
                    result.append(Project(**dict(row)))
        result_msg = f"{len(result)} project"
        logger.info(f"select_projects() -> {result_msg}")
        return result

    @overrides
    async def select_project_by_uid(self, uid: int) -> Project:
        query = SELECT_PROJECT_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found project: {params_msg}")
        result = Project(**dict(row))
        assert result.uid == uid
        logger.info(f"select_project_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_project_by_group_uid(self, group_uid: int) -> List[Project]:
        result: List[Project] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PROJECT_BY_GROUP_ID
                async for row in conn.cursor(query, group_uid):
                    item = Project(**dict(row))
                    assert item.group_uid == group_uid
                    result.append(item)
        params_msg = f"group_uid={group_uid}"
        result_msg = f"{len(result)} project"
        logger.info(f"select_project_by_group_uid({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def select_projects_count(self) -> int:
        query = SELECT_PROJECT_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = int(row.get("count", 0))
        logger.info(f"select_projects_count() -> {result}")
        return result
