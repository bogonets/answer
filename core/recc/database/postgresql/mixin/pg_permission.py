# -*- coding: utf-8 -*-

from typing import Optional, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.permission import Permission
from recc.database.interfaces.db_permission import DbPermission
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.permission import (
    INSERT_PERMISSION,
    DELETE_PERMISSION_BY_UID,
    SELECT_PERMISSION_UID_BY_SLUG,
    SELECT_PERMISSION_SLUG_BY_UID,
    SELECT_PERMISSION_BY_SLUG,
    SELECT_PERMISSION_BY_UID,
    SELECT_PERMISSION_ALL,
    SELECT_PERMISSION_BY_ROLE_UID,
    SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP,
    SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_AND_PROJECT,
)


class PgPermission(DbPermission, PgBase):
    @overrides
    async def insert_permission(
        self,
        slug: str,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else today()
        uid = await self.fetch_val(INSERT_PERMISSION, slug, created)
        logger.info(f"insert_permission(slug={slug}) -> {uid}")
        return uid

    @overrides
    async def delete_permission(self, uid: int) -> None:
        query = DELETE_PERMISSION_BY_UID
        await self.execute(query, uid)
        logger.info(f"delete_permission(uid={uid}) ok.")

    @overrides
    async def select_permission_uid_by_slug(self, slug: str) -> int:
        query = SELECT_PERMISSION_UID_BY_SLUG
        row = await self.fetch_row(query, slug)
        params_msg = f"slug={slug}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = int(row["uid"])
        logger.info(f"select_permission_uid_by_slug({params_msg}) -> {result}")
        return result

    @overrides
    async def select_permission_slug_by_uid(self, uid: int) -> str:
        query = SELECT_PERMISSION_SLUG_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = str(row["slug"])
        logger.info(f"select_permission_slug_by_uid({params_msg}) -> {result}")
        return result

    @overrides
    async def select_permission_by_slug(self, slug: str) -> Permission:
        query = SELECT_PERMISSION_BY_SLUG
        row = await self.fetch_row(query, slug)
        params_msg = f"slug={slug}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = Permission(**dict(row))
        logger.info(f"select_permission_by_slug({params_msg}) ok.")
        return result

    @overrides
    async def select_permission_by_uid(self, uid: int) -> Permission:
        query = SELECT_PERMISSION_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = Permission(**dict(row))
        logger.info(f"select_permission_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_permission_all(self) -> List[Permission]:
        query = SELECT_PERMISSION_ALL
        rows = await self.fetch(query)
        return [Permission(**dict(row)) for row in rows]

    @overrides
    async def select_permission_by_role_uid(self, role_uid: int) -> List[Permission]:
        query = SELECT_PERMISSION_BY_ROLE_UID
        rows = await self.fetch(query, role_uid)
        return [Permission(**dict(row)) for row in rows]

    @overrides
    async def select_appropriate_permission_by_user_and_group(
        self, user_uid: int, group_uid: int
    ) -> List[Permission]:
        query = SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP
        rows = await self.fetch(query, user_uid, group_uid)
        return [Permission(**dict(row)) for row in rows]

    @overrides
    async def select_appropriate_permission_by_user_and_group_and_project(
        self, user_uid: int, group_uid: int, project_uid: int
    ) -> List[Permission]:
        query = SELECT_APPROPRIATE_PERMISSION_BY_USER_AND_GROUP_AND_PROJECT
        rows = await self.fetch(query, user_uid, group_uid, project_uid)
        return [Permission(**dict(row)) for row in rows]
