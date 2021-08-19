# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.permission import Permission
from recc.database.interfaces.db_permission import DbPermission
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.permission import (
    INSERT_PERMISSION,
    DELETE_PERMISSION_BY_UID,
    SELECT_PERMISSION_UID_BY_NAME,
    SELECT_PERMISSION_NAME_BY_UID,
    SELECT_PERMISSION_BY_UID,
    SELECT_PERMISSION_ALL,
    SELECT_BEST_PERMISSION_OF_PROJECT_NO_COMMENT,
    get_update_permission_query_by_uid,
)


class PgPermission(DbPermission, PgBase):
    @overrides
    async def insert_permission(
        self,
        name: str,
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
        created_at=datetime.utcnow(),
    ) -> int:
        uid = await self.fetch_val(
            INSERT_PERMISSION,
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
            created_at,
        )
        logger.info(f"insert_permission(name={name}) -> {uid}")
        return uid

    @overrides
    async def update_permission_by_uid(
        self,
        uid: int,
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
        updated_at=datetime.utcnow(),
    ) -> None:
        query, args = get_update_permission_query_by_uid(
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
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        params_msg = f"name={name}"
        logger.info(f"update_permission_by_uid({params_msg}) ok.")

    @overrides
    async def delete_permission_by_uid(self, uid: int) -> None:
        query = DELETE_PERMISSION_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_permission_by_uid({params_msg}) ok.")

    @overrides
    async def select_permission_uid_by_name(self, name: str) -> int:
        query = SELECT_PERMISSION_UID_BY_NAME
        row = await self.fetch_row(query, name)
        params_msg = f"name={name}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = int(row["uid"])
        logger.info(f"select_permission_uid_by_name({params_msg}) -> {result}")
        return result

    @overrides
    async def select_permission_name_by_uid(self, uid: int) -> str:
        query = SELECT_PERMISSION_NAME_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = str(row["name"])
        logger.info(f"select_permission_name_by_uid({params_msg}) -> {result}")
        return result

    @overrides
    async def select_permission_by_uid(self, uid: int) -> Permission:
        query = SELECT_PERMISSION_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = Permission(**dict(row))
        result.uid = uid
        logger.info(f"select_permission_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_permissions(self) -> List[Permission]:
        result: List[Permission] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PERMISSION_ALL
                async for row in conn.cursor(query):
                    result.append(Permission(**dict(row)))
        result_msg = f"{len(result)} permissions"
        logger.info(f"select_permissions() -> {result_msg}")
        return result

    @overrides
    async def select_project_permission_by_uid(
        self, user_uid: int, project_uid: int
    ) -> Permission:
        query = SELECT_BEST_PERMISSION_OF_PROJECT_NO_COMMENT
        row = await self.fetch_row(query, user_uid, project_uid)
        params_msg = f"user_uid={user_uid},project_uid={project_uid}"
        if not row:
            raise RuntimeError(f"Not found permission: {params_msg}")
        result = Permission(**dict(row))
        logger.info(f"select_project_permission_by_uid({params_msg}) ok.")
        return result
