# -*- coding: utf-8 -*-

from functools import reduce
from datetime import datetime
from typing import Optional
from asyncpg.pool import Pool

from recc.exception.recc_error import ReccNotReadyError
from recc.database.async_db_interface import AsyncDatabaseInterface
from recc.database.postgresql.query.tables import CREATE_TABLES, DROP_TABLES
from recc.database.postgresql.query.indices import CREATE_INDICES, DROP_INDICES
from recc.database.postgresql.query.views import CREATE_VIEWS, DROP_VIEWS
from recc.database.postgresql.query.info import SAFE_INSERT_INFO_DB_VERSION
from recc.database.postgresql.query.group import (
    SAFE_INSERT_GROUP_ANONYMOUS,
    SELECT_GROUP_ANONYMOUS_UID,
)
from recc.database.postgresql.query.permission import (
    SAFE_INSERT_PERMISSION_DEFAULTS,
    SELECT_PERMISSION_GUEST_UID,
    SELECT_PERMISSION_REPORTER_UID,
    SELECT_PERMISSION_OPERATOR_UID,
    SELECT_PERMISSION_MAINTAINER_UID,
)
from recc.database.postgresql.mixin.async_pg_group import AsyncPgGroup
from recc.database.postgresql.mixin.async_pg_group_member import AsyncPgGroupMember
from recc.database.postgresql.mixin.async_pg_info import AsyncPgInfo
from recc.database.postgresql.mixin.async_pg_layout import AsyncPgLayout
from recc.database.postgresql.mixin.async_pg_permission import AsyncPgPermission
from recc.database.postgresql.mixin.async_pg_port import AsyncPgPort
from recc.database.postgresql.mixin.async_pg_project import AsyncPgProject
from recc.database.postgresql.mixin.async_pg_project_member import AsyncPgProjectMember
from recc.database.postgresql.mixin.async_pg_task import AsyncPgTask
from recc.database.postgresql.mixin.async_pg_user import AsyncPgUser
from recc.database.postgresql.mixin.async_pg_widget import AsyncPgWidget
from recc.database.postgresql.pg_utils import (
    connect_and_create_if_not_exists,
    drop_database,
)
from recc.variables.database import DEFAULT_TIMEOUT_SECONDS
from recc.log.logging import recc_database_logger as logger

EX_KEY_TIMEOUT = "timeout"


class AsyncPostgresqlDatabase(
    AsyncPgGroup,
    AsyncPgGroupMember,
    AsyncPgInfo,
    AsyncPgLayout,
    AsyncPgPermission,
    AsyncPgPort,
    AsyncPgProject,
    AsyncPgProjectMember,
    AsyncPgTask,
    AsyncPgUser,
    AsyncPgWidget,
    AsyncDatabaseInterface,
):
    """
    PostgreSQL Database class.

    :param kwargs:
        - timeout: Optional timeout value in seconds.
    """

    _pool: Optional[Pool] = None

    def __init__(
        self,
        db_host: Optional[str] = None,
        db_port: Optional[int] = None,
        db_user: Optional[str] = None,
        db_pw: Optional[str] = None,
        db_name: Optional[str] = None,
        **kwargs,
    ):
        self._db_host = db_host
        self._db_port = db_port
        self._db_user = db_user
        self._db_pw = db_pw
        self._db_name = db_name
        self._timeout = float(kwargs.get(EX_KEY_TIMEOUT, DEFAULT_TIMEOUT_SECONDS))

        self._anonymous_group_uid: Optional[int] = None
        self._guest_permission_uid: Optional[int] = None
        self._reporter_permission_uid: Optional[int] = None
        self._operator_permission_uid: Optional[int] = None
        self._maintainer_permission_uid: Optional[int] = None

    def is_open(self) -> bool:
        return self._pool is not None

    async def open(self) -> None:
        self._pool = await connect_and_create_if_not_exists(
            host=self._db_host,
            port=self._db_port,
            user=self._db_user,
            password=self._db_pw,
            database=self._db_name,
            command_timeout=self._timeout,
        )

    async def close(self) -> None:
        assert self._pool
        await self._pool.close()
        self._pool = None

    async def drop(self) -> None:
        await drop_database(
            self._db_host,
            self._db_port,
            self._db_user,
            self._db_pw,
            self._db_name,
        )

    async def create_tables(self, created_at=datetime.utcnow()) -> None:
        all_create = CREATE_TABLES + CREATE_INDICES + CREATE_VIEWS
        async with self.conn() as conn:
            async with conn.transaction():
                await conn.execute(reduce(lambda x, y: x + y, all_create))
                await conn.execute(SAFE_INSERT_INFO_DB_VERSION, created_at)
                await conn.execute(SAFE_INSERT_GROUP_ANONYMOUS, created_at)
                for perm_query in SAFE_INSERT_PERMISSION_DEFAULTS:
                    await conn.execute(perm_query, created_at)

    async def drop_tables(self) -> None:
        all_drop = DROP_TABLES + DROP_INDICES + DROP_VIEWS
        all_drop_reverse = all_drop[::-1]
        await self.execute(reduce(lambda x, y: x + y, all_drop_reverse))

    async def _fetch_uid(self, query, *args, **kwargs) -> int:
        row = await self.fetch_row(query, *args, **kwargs)
        assert row and len(row) == 1
        return int(row["uid"])

    async def _get_anonymous_group_uid(self) -> int:
        return await self._fetch_uid(SELECT_GROUP_ANONYMOUS_UID)

    async def _get_guest_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_GUEST_UID)

    async def _get_reporter_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_REPORTER_UID)

    async def _get_operator_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_OPERATOR_UID)

    async def _get_maintainer_permission_uid(self) -> int:
        return await self._fetch_uid(SELECT_PERMISSION_MAINTAINER_UID)

    async def update_cache(self) -> None:
        self._anonymous_group_uid = await self._get_anonymous_group_uid()
        self._guest_permission_uid = await self._get_guest_permission_uid()
        self._reporter_permission_uid = await self._get_reporter_permission_uid()
        self._operator_permission_uid = await self._get_operator_permission_uid()
        self._maintainer_permission_uid = await self._get_maintainer_permission_uid()
        logger.info("update_cache() ok.")

    def get_anonymous_group_uid(self) -> int:
        if self._anonymous_group_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._anonymous_group_uid

    def get_guest_permission_uid(self) -> int:
        if self._guest_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._guest_permission_uid

    def get_reporter_permission_uid(self) -> int:
        if self._reporter_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._reporter_permission_uid

    def get_operator_permission_uid(self) -> int:
        if self._operator_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._operator_permission_uid

    def get_maintainer_permission_uid(self) -> int:
        if self._maintainer_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._maintainer_permission_uid
