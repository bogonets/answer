# -*- coding: utf-8 -*-

from functools import reduce
from datetime import datetime
from typing import Optional
from asyncpg.pool import Pool
from overrides import overrides

from recc.exception.recc_error import ReccNotReadyError
from recc.database.interfaces.db_interface import DbInterface
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
from recc.database.postgresql.mixin.pg_group import PgGroup
from recc.database.postgresql.mixin.pg_group_member import PgGroupMember
from recc.database.postgresql.mixin.pg_info import PgInfo
from recc.database.postgresql.mixin.pg_layout import PgLayout
from recc.database.postgresql.mixin.pg_permission import PgPermission
from recc.database.postgresql.mixin.pg_port import PgPort
from recc.database.postgresql.mixin.pg_project import PgProject
from recc.database.postgresql.mixin.pg_project_member import PgProjectMember
from recc.database.postgresql.mixin.pg_task import PgTask
from recc.database.postgresql.mixin.pg_user import PgUser
from recc.database.postgresql.mixin.pg_widget import PgWidget
from recc.database.postgresql.pg_utils import (
    connect_and_create_if_not_exists,
    drop_database,
)
from recc.variables.database import DEFAULT_TIMEOUT_SECONDS
from recc.log.logging import recc_database_logger as logger

EX_KEY_TIMEOUT = "timeout"


class PgDb(
    DbInterface,  # Include: DbOpen, DbMisc
    PgGroup,
    PgGroupMember,
    PgInfo,
    PgLayout,
    PgPermission,
    PgPort,
    PgProject,
    PgProjectMember,
    PgTask,
    PgUser,
    PgWidget,
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

    @overrides
    def is_open(self) -> bool:
        return self._pool is not None

    @overrides
    async def open(self) -> None:
        self._pool = await connect_and_create_if_not_exists(
            host=self._db_host,
            port=self._db_port,
            user=self._db_user,
            password=self._db_pw,
            database=self._db_name,
            command_timeout=self._timeout,
        )

    @overrides
    async def close(self) -> None:
        assert self._pool
        await self._pool.close()
        self._pool = None

    @overrides
    async def drop(self) -> None:
        await drop_database(
            self._db_host,
            self._db_port,
            self._db_user,
            self._db_pw,
            self._db_name,
        )

    @overrides
    async def create_tables(self, created_at=datetime.utcnow()) -> None:
        all_create = CREATE_TABLES + CREATE_INDICES + CREATE_VIEWS
        async with self.conn() as conn:
            async with conn.transaction():
                await conn.execute(reduce(lambda x, y: x + y, all_create))
                await conn.execute(SAFE_INSERT_INFO_DB_VERSION, created_at)
                await conn.execute(SAFE_INSERT_GROUP_ANONYMOUS, created_at)
                for perm_query in SAFE_INSERT_PERMISSION_DEFAULTS:
                    await conn.execute(perm_query, created_at)

    @overrides
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

    @overrides
    async def update_cache(self) -> None:
        self._anonymous_group_uid = await self._get_anonymous_group_uid()
        self._guest_permission_uid = await self._get_guest_permission_uid()
        self._reporter_permission_uid = await self._get_reporter_permission_uid()
        self._operator_permission_uid = await self._get_operator_permission_uid()
        self._maintainer_permission_uid = await self._get_maintainer_permission_uid()
        logger.info("update_cache() ok.")

    @overrides
    def get_anonymous_group_uid(self) -> int:
        if self._anonymous_group_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._anonymous_group_uid

    @overrides
    def get_guest_permission_uid(self) -> int:
        if self._guest_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._guest_permission_uid

    @overrides
    def get_reporter_permission_uid(self) -> int:
        if self._reporter_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._reporter_permission_uid

    @overrides
    def get_operator_permission_uid(self) -> int:
        if self._operator_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._operator_permission_uid

    @overrides
    def get_maintainer_permission_uid(self) -> int:
        if self._maintainer_permission_uid is None:
            raise ReccNotReadyError("The cache has not been updated")
        return self._maintainer_permission_uid
