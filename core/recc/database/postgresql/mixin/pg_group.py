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
    UPDATE_GROUP_NAME_BY_UID,
    UPDATE_GROUP_DESCRIPTION_BY_UID,
    UPDATE_GROUP_DESCRIPTION_BY_NAME,
    UPDATE_GROUP_EXTRA_BY_UID,
    UPDATE_GROUP_EXTRA_BY_NAME,
    UPDATE_GROUP_FEATURES_BY_UID,
    UPDATE_GROUP_FEATURES_BY_NAME,
    DELETE_GROUP_BY_UID,
    DELETE_GROUP_BY_NAME,
    SELECT_GROUP_UID_BY_NAME,
    SELECT_GROUP_BY_UID,
    SELECT_GROUP_BY_NAME,
    SELECT_GROUP_ALL,
    SELECT_GROUP_COUNT,
    get_update_group_query_by_uid,
)


class PgGroup(DbGroup, PgBase):
    @overrides
    async def create_group(
        self,
        name: str,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_GROUP
        await self.execute(query, name, description, features, extra, created_at)
        params_msg = f"name={name}"
        logger.info(f"create_group({params_msg}) ok.")

    @overrides
    async def update_group_name_by_uid(
        self, uid: int, name: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_GROUP_NAME_BY_UID
        await self.execute(query, uid, name, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_group_name_by_uid({params_msg}) ok.")

    @overrides
    async def update_group_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_GROUP_DESCRIPTION_BY_UID
        await self.execute(query, uid, description, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_group_description_by_uid({params_msg}) ok.")

    @overrides
    async def update_group_description_by_name(
        self, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_GROUP_DESCRIPTION_BY_NAME
        await self.execute(query, name, description, updated_at)
        params_msg = f"name={name}"
        logger.info(f"update_group_description_by_name({params_msg}) ok.")

    @overrides
    async def update_group_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_GROUP_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_group_extra_by_uid({params_msg}) ok.")

    @overrides
    async def update_group_extra_by_name(
        self, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_GROUP_EXTRA_BY_NAME
        await self.execute(query, name, extra, updated_at)
        params_msg = f"name={name}"
        logger.info(f"update_group_extra_by_name({params_msg}) ok.")

    @overrides
    async def update_group_features_by_uid(
        self, uid: int, features: List[str], updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_GROUP_FEATURES_BY_UID
        await self.execute(query, uid, features, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_group_features_by_uid({params_msg}) ok.")

    @overrides
    async def update_group_features_by_name(
        self, name: str, features: List[str], updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_GROUP_FEATURES_BY_NAME
        await self.execute(query, name, features, updated_at)
        params_msg = f"name={name}"
        logger.info(f"update_group_features_by_name({params_msg}) ok.")

    @overrides
    async def update_group_by_uid(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        query, args = get_update_group_query_by_uid(
            uid=uid,
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
    async def delete_group_by_name(self, name: str) -> None:
        query = DELETE_GROUP_BY_NAME
        await self.execute(query, name)
        params_msg = f"name={name}"
        logger.info(f"delete_group_by_name({params_msg}) ok.")

    @overrides
    async def get_group_uid_by_name(self, name: str) -> int:
        query = SELECT_GROUP_UID_BY_NAME
        row = await self.fetch_row(query, name)
        params_msg = f"name={name}"
        if not row:
            raise RuntimeError(f"Not found group: {params_msg}")
        assert row and len(row) == 1
        result = int(row.get("uid"))
        logger.info(f"get_group_uid_by_name({params_msg}) -> {result}")
        return result

    @overrides
    async def get_group_by_uid(self, uid: int) -> Group:
        query = SELECT_GROUP_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found group: {params_msg}")
        result = Group(**dict(row))
        result.uid = uid
        logger.info(f"get_group_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def get_group_by_name(self, name: str) -> Group:
        query = SELECT_GROUP_BY_NAME
        row = await self.fetch_row(query, name)
        params_msg = f"name={name}"
        if not row:
            raise RuntimeError(f"Not found group: {params_msg}")
        result = Group(**dict(row))
        result.name = name
        logger.info(f"get_group_by_name({params_msg}) ok.")
        return result

    @overrides
    async def get_groups(self) -> List[Group]:
        result: List[Group] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_GROUP_ALL
                async for row in conn.cursor(query):
                    result.append(Group(**dict(row)))
        result_msg = f"{len(result)} groups"
        logger.info(f"get_groups() -> {result_msg}")
        return result

    @overrides
    async def get_groups_count(self) -> int:
        query = SELECT_GROUP_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = int(row.get("count", 0))
        logger.info(f"get_groups_count() -> {result}")
        return result
