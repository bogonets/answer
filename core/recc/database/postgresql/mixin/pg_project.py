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
    UPDATE_PROJECT_DESCRIPTION_BY_UID,
    UPDATE_PROJECT_DESCRIPTION_BY_GROUP_UID_AND_SLUG,
    UPDATE_PROJECT_EXTRA_BY_UID,
    UPDATE_PROJECT_EXTRA_BY_GROUP_UID_AND_SLUG,
    UPDATE_PROJECT_FEATURES_BY_UID,
    UPDATE_PROJECT_FEATURES_BY_GROUP_UID_AND_SLUG,
    DELETE_PROJECT_BY_UID,
    DELETE_PROJECT_BY_GROUP_UID_AND_SLUG,
    SELECT_PROJECT_BY_UID,
    SELECT_PROJECT_BY_GROUP_ID_AND_SLUG,
    SELECT_PROJECT_BY_GROUP_ID,
    SELECT_PROJECT_BY_FULLPATH,
    SELECT_PROJECT_UID_BY_FULLPATH,
    SELECT_PROJECT_COUNT,
    get_update_project_query_by_uid,
)


class PgProject(DbProject, PgBase):
    @overrides
    async def create_project(
        self,
        group_uid: int,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_PROJECT
        await self.execute(
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
        logger.info(f"create_project({params_msg}) ok.")

    @overrides
    async def update_project_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_DESCRIPTION_BY_UID
        await self.execute(query, uid, description, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_project_description_by_uid({params_msg}) ok.")

    @overrides
    async def update_project_description_by_slug(
        self, group_uid: int, slug: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_DESCRIPTION_BY_GROUP_UID_AND_SLUG
        await self.execute(query, group_uid, slug, description, updated_at)
        params_msg = f"group_uid={group_uid},slug={slug}"
        logger.info(f"update_project_description_by_slug({params_msg}) ok.")

    @overrides
    async def update_project_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        logger.info(f"update_project_extra_by_uid(uid={uid}) ok.")

    @overrides
    async def update_project_extra_by_slug(
        self, group_uid: int, slug: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_EXTRA_BY_GROUP_UID_AND_SLUG
        await self.execute(query, group_uid, slug, extra, updated_at)
        params_msg = f"group_uid={group_uid},slug={slug}"
        logger.info(f"update_project_extra_by_slug({params_msg}) ok.")

    @overrides
    async def update_project_features_by_uid(
        self, uid: int, features: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_FEATURES_BY_UID
        await self.execute(query, uid, features, updated_at)
        logger.info(f"update_project_features_by_uid(uid={uid}) ok.")

    @overrides
    async def update_project_features_by_slug(
        self,
        group_uid: int,
        slug: str,
        features: List[str],
        updated_at=datetime.utcnow(),
    ) -> None:
        query = UPDATE_PROJECT_FEATURES_BY_GROUP_UID_AND_SLUG
        await self.execute(query, group_uid, slug, features, updated_at)
        params_msg = f"group_uid={group_uid},slug={slug}"
        logger.info(f"update_project_features_by_slug({params_msg}) ok.")

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
    async def delete_project_by_slug(self, group_uid: int, slug: str) -> None:
        query = DELETE_PROJECT_BY_GROUP_UID_AND_SLUG
        await self.execute(query, group_uid, slug)
        params_msg = f"group_uid={group_uid},slug={slug}"
        logger.info(f"delete_project_by_slug({params_msg}) ok.")

    @overrides
    async def get_project_by_uid(self, uid: int) -> Project:
        query = SELECT_PROJECT_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found project: {params_msg}")
        result = Project(**dict(row))
        assert result.uid == uid
        logger.info(f"get_project_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def get_project_by_slug(self, group_uid: int, slug: str) -> Project:
        query = SELECT_PROJECT_BY_GROUP_ID_AND_SLUG
        row = await self.fetch_row(query, group_uid, slug)
        params_msg = f"group_uid={group_uid},slug={slug}"
        if not row:
            raise RuntimeError(f"Not found project: {params_msg}")
        result = Project(**dict(row))
        assert result.group_uid == group_uid
        assert result.slug == slug
        logger.info(f"get_project_by_slug({params_msg}) ok.")
        return result

    @overrides
    async def get_project_by_group_uid(self, group_uid: int) -> List[Project]:
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
        logger.info(f"get_project_by_group_uid({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def get_project_by_fullpath(
        self, group_slug: str, project_slug: str
    ) -> Project:
        query = SELECT_PROJECT_BY_FULLPATH
        row = await self.fetch_row(query, group_slug, project_slug)
        params_msg = f"group={group_slug},project={project_slug}"
        if not row:
            raise RuntimeError(f"Not found project: {params_msg}")
        if row.get("uid") is None:
            raise RuntimeError(f"Not found project: {params_msg}")
        result = Project(**dict(row))
        assert result.slug == project_slug
        logger.info(f"get_project_by_fullpath({params_msg}) ok.")
        return result

    @overrides
    async def get_project_uid_by_fullpath(
        self, group_slug: str, project_slug: str
    ) -> int:
        query = SELECT_PROJECT_UID_BY_FULLPATH
        row = await self.fetch_row(query, group_slug, project_slug)
        params_msg = f"group={group_slug},project={project_slug}"
        if not row:
            raise RuntimeError(f"Not found project: {params_msg}")
        result = row.get("uid")
        if result is None:
            raise RuntimeError(f"Not found project: {params_msg}")
        logger.info(f"get_project_uid_by_fullpath({params_msg}) -> {result}")
        return result

    @overrides
    async def get_projects_count(self) -> int:
        query = SELECT_PROJECT_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = int(row.get("count", 0))
        logger.info(f"get_projects_count() -> {result}")
        return result
