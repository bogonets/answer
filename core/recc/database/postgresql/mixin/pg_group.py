# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.group import Group
from recc.database.interfaces.db_group import DbGroup
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.group import (
    INSERT_GROUP,
    DELETE_GROUP_BY_UID,
    SELECT_GROUP_UID_BY_SLUG,
    SELECT_GROUP_SLUG_BY_UID,
    SELECT_GROUP_BY_UID,
    SELECT_GROUP_ALL,
    SELECT_GROUP_COUNT,
    get_update_group_query_by_uid,
)


class PgGroup(DbGroup, PgBase):
    @overrides
    async def insert_group(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_GROUP
        await self.execute(query, slug, name, description, features, extra, created_at)
        params_msg = f"slug={slug}"
        logger.info(f"insert_group({params_msg}) ok.")

    @overrides
    async def update_group_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        query, args = get_update_group_query_by_uid(
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
        logger.info(f"update_group_by_uid({params_msg}) ok.")

    @overrides
    async def delete_group_by_uid(self, uid: int) -> None:
        query = DELETE_GROUP_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_group_by_uid({params_msg}) ok.")

    @overrides
    async def select_group_uid_by_slug(self, slug: str) -> int:
        query = SELECT_GROUP_UID_BY_SLUG
        row = await self.fetch_row(query, slug)
        params_msg = f"slug={slug}"
        if not row:
            raise RuntimeError(f"Not found group: {params_msg}")
        assert row and len(row) == 1
        result = int(row.get("uid"))
        logger.info(f"select_group_uid_by_slug({params_msg}) -> {result}")
        return result

    @overrides
    async def select_group_slug_by_uid(self, uid: int) -> str:
        query = SELECT_GROUP_SLUG_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found group: {params_msg}")
        assert row and len(row) == 1
        result = row.get("slug")
        logger.info(f"select_group_slug_by_uid({params_msg}) -> {result}")
        return result

    @overrides
    async def select_group_by_uid(self, uid: int) -> Group:
        query = SELECT_GROUP_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found group: {params_msg}")
        result = Group(**dict(row))
        result.uid = uid
        logger.info(f"select_group_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_groups(self) -> List[Group]:
        result: List[Group] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_ALL
                async for row in conn.cursor(query):
                    result.append(Group(**dict(row)))
        result_msg = f"{len(result)} groups"
        logger.info(f"select_groups() -> {result_msg}")
        return result

    @overrides
    async def select_groups_count(self) -> int:
        query = SELECT_GROUP_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = int(row.get("count", 0))
        logger.info(f"select_groups_count() -> {result}")
        return result
