# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.project import Project
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
from recc.database.postgresql.query.project import (
    INSERT_PROJECT,
    UPDATE_PROJECT_DESCRIPTION_BY_UID,
    UPDATE_PROJECT_DESCRIPTION_BY_GROUP_UID_AND_NAME,
    UPDATE_PROJECT_EXTRA_BY_UID,
    UPDATE_PROJECT_EXTRA_BY_GROUP_UID_AND_NAME,
    DELETE_PROJECT_BY_UID,
    DELETE_PROJECT_BY_GROUP_UID_AND_NAME,
    SELECT_PROJECT_BY_UID,
    SELECT_PROJECT_BY_GROUP_ID_AND_NAME,
    SELECT_PROJECT_BY_GROUP_ID,
    SELECT_PROJECT_BY_FULLPATH,
    SELECT_PROJECT_UID_BY_FULLPATH,
)


class AsyncPgProject(AsyncPgBase):
    async def create_project(
        self,
        group_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_PROJECT
        await self.execute(query, group_uid, name, description, extra, created_at)
        params_msg = f"group_uid={group_uid},name={name}"
        logger.info(f"create_project({params_msg}) ok.")

    async def update_project_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_DESCRIPTION_BY_UID
        await self.execute(query, uid, description, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_project_description_by_uid({params_msg}) ok.")

    async def update_project_description_by_name(
        self, group_uid: int, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_DESCRIPTION_BY_GROUP_UID_AND_NAME
        await self.execute(query, group_uid, name, description, updated_at)
        params_msg = f"group_uid={group_uid},name={name}"
        logger.info(f"update_project_description_by_name({params_msg}) ok.")

    async def update_project_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        logger.info(f"update_project_extra_by_uid(uid={uid}) ok.")

    async def update_project_extra_by_name(
        self, group_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_PROJECT_EXTRA_BY_GROUP_UID_AND_NAME
        await self.execute(query, group_uid, name, extra, updated_at)
        params_msg = f"group_uid={group_uid},name={name}"
        logger.info(f"update_project_extra_by_name({params_msg}) ok.")

    async def delete_project_by_uid(self, uid: int) -> None:
        query = DELETE_PROJECT_BY_UID
        await self.execute(query, uid)
        logger.info(f"delete_project_by_uid(uid={uid}) ok.")

    async def delete_project_by_name(self, group_uid: int, name: str) -> None:
        query = DELETE_PROJECT_BY_GROUP_UID_AND_NAME
        await self.execute(query, group_uid, name)
        params_msg = f"group_uid={group_uid},name={name}"
        logger.info(f"delete_project_by_name({params_msg}) ok.")

    async def get_project_by_uid(self, uid: int) -> Project:
        query = SELECT_PROJECT_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise ReccNotFoundError(f"Not found project: {params_msg}")
        result = Project(**dict(row))
        assert result.uid == uid
        logger.info(f"get_project_by_uid({params_msg}) ok.")
        return result

    async def get_project_by_name(self, group_uid: int, name: str) -> Project:
        query = SELECT_PROJECT_BY_GROUP_ID_AND_NAME
        row = await self.fetch_row(query, group_uid, name)
        params_msg = f"group_uid={group_uid},name={name}"
        if not row:
            raise ReccNotFoundError(f"Not found project: {params_msg}")
        result = Project(**dict(row))
        assert result.group_uid == group_uid
        assert result.name == name
        logger.info(f"get_project_by_name({params_msg}) ok.")
        return result

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

    async def get_project_by_fullpath(
        self, group_name: str, project_name: str
    ) -> Project:
        query = SELECT_PROJECT_BY_FULLPATH
        row = await self.fetch_row(query, group_name, project_name)
        params_msg = f"group={group_name},project={project_name}"
        if not row:
            raise ReccNotFoundError(f"Not found project: {params_msg}")
        if row.get("uid") is None:
            raise ReccNotFoundError(f"Not found project: {params_msg}")
        result = Project(**dict(row))
        assert result.name == project_name
        logger.info(f"get_project_by_fullpath({params_msg}) ok.")
        return result

    async def get_project_uid_by_fullpath(
        self, group_name: str, project_name: str
    ) -> int:
        query = SELECT_PROJECT_UID_BY_FULLPATH
        row = await self.fetch_row(query, group_name, project_name)
        params_msg = f"group={group_name},project={project_name}"
        if not row:
            raise ReccNotFoundError(f"Not found project: {params_msg}")
        result = row.get("uid")
        if result is None:
            raise ReccNotFoundError(f"Not found project: {params_msg}")
        logger.info(f"get_project_uid_by_fullpath({params_msg}) -> {result}")
        return result
