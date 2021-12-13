# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.role import Role
from recc.database.interfaces.db_role import DbRole
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.role import (
    INSERT_ROLE,
    DELETE_ROLE_BY_UID,
    SELECT_ROLE_UID_BY_SLUG,
    SELECT_ROLE_SLUG_BY_UID,
    SELECT_ROLE_BY_UID,
    SELECT_ROLE_LOCK_BY_UID,
    SELECT_ROLE_ALL,
    SELECT_ROLE_BY_USER_UID_AND_GROUP_UID,
    SELECT_ROLE_BY_USER_UID_AND_PROJECT_UID,
    get_update_role_query_by_uid,
)


class PgRole(DbRole, PgBase):
    @overrides
    async def insert_role(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout=False,
        w_layout=False,
        r_storage=False,
        w_storage=False,
        r_manager=False,
        w_manager=False,
        r_graph=False,
        w_graph=False,
        r_member=False,
        w_member=False,
        r_setting=False,
        w_setting=False,
        hidden=False,
        lock=False,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else today()
        uid = await self.fetch_val(
            INSERT_ROLE,
            slug,
            name,
            description,
            features,
            extra,
            r_layout,
            w_layout,
            r_storage,
            w_storage,
            r_manager,
            w_manager,
            r_graph,
            w_graph,
            r_member,
            w_member,
            r_setting,
            w_setting,
            hidden,
            lock,
            created,
        )
        logger.info(f"insert_role(name={name}) -> {uid}")
        return uid

    @overrides
    async def update_role_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout: Optional[bool] = None,
        w_layout: Optional[bool] = None,
        r_storage: Optional[bool] = None,
        w_storage: Optional[bool] = None,
        r_manager: Optional[bool] = None,
        w_manager: Optional[bool] = None,
        r_graph: Optional[bool] = None,
        w_graph: Optional[bool] = None,
        r_member: Optional[bool] = None,
        w_member: Optional[bool] = None,
        r_setting: Optional[bool] = None,
        w_setting: Optional[bool] = None,
        hidden: Optional[bool] = None,
        lock: Optional[bool] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query, args = get_update_role_query_by_uid(
            slug=slug,
            uid=uid,
            name=name,
            description=description,
            features=features,
            extra=extra,
            r_layout=r_layout,
            w_layout=w_layout,
            r_storage=r_storage,
            w_storage=w_storage,
            r_manager=r_manager,
            w_manager=w_manager,
            r_graph=r_graph,
            w_graph=w_graph,
            r_member=r_member,
            w_member=w_member,
            r_setting=r_setting,
            w_setting=w_setting,
            hidden=hidden,
            lock=lock,
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        logger.info(f"update_role_by_uid(slug={slug}) ok.")

    @overrides
    async def delete_role_by_uid(self, uid: int) -> None:
        query = DELETE_ROLE_BY_UID
        await self.execute(query, uid)
        logger.info(f"delete_role_by_uid(uid={uid}) ok.")

    @overrides
    async def select_role_uid_by_slug(self, slug: str) -> int:
        query = SELECT_ROLE_UID_BY_SLUG
        row = await self.fetch_row(query, slug)
        params_msg = f"slug={slug}"
        if not row:
            raise RuntimeError(f"Not found role: {params_msg}")
        result = int(row["uid"])
        logger.info(f"select_role_uid_by_slug({params_msg}) -> {result}")
        return result

    @overrides
    async def select_role_slug_by_uid(self, uid: int) -> str:
        query = SELECT_ROLE_SLUG_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found role: {params_msg}")
        result = str(row["slug"])
        logger.info(f"select_role_slug_by_uid({params_msg}) -> {result}")
        return result

    @overrides
    async def select_role_by_uid(self, uid: int) -> Role:
        query = SELECT_ROLE_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found role: {params_msg}")
        result = Role(**dict(row))
        result.uid = uid
        logger.info(f"select_role_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_role_lock_by_uid(self, uid: int) -> bool:
        query = SELECT_ROLE_LOCK_BY_UID
        lock = await self.fetch_val(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"select_role_lock_by_uid({params_msg}) -> {lock}")
        return lock

    @overrides
    async def select_role_all(self) -> List[Role]:
        result: List[Role] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_ROLE_ALL
                async for row in conn.cursor(query):
                    result.append(Role(**dict(row)))
        result_msg = f"{len(result)} roles"
        logger.info(f"select_roles() -> {result_msg}")
        return result

    @overrides
    async def select_role_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> Role:
        query = SELECT_ROLE_BY_USER_UID_AND_GROUP_UID
        row = await self.fetch_row(query, user_uid, group_uid)
        params_msg = f"user_uid={user_uid},group_uid={group_uid}"
        if not row:
            raise RuntimeError(f"Not found role: {params_msg}")
        result = Role(**dict(row))
        logger.info(f"select_role_by_user_uid_and_group_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_role_by_user_uid_and_project_uid(
        self, user_uid: int, project_uid: int
    ) -> Role:
        query = SELECT_ROLE_BY_USER_UID_AND_PROJECT_UID
        row = await self.fetch_row(query, user_uid, project_uid)
        params_msg = f"user_uid={user_uid},project_uid={project_uid}"
        if not row:
            raise RuntimeError(f"Not found role: {params_msg}")
        result = Role(**dict(row))
        logger.info(f"select_role_by_user_uid_and_project_uid({params_msg}) ok.")
        return result
