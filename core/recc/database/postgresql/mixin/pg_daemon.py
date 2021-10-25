# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.daemon import Daemon
from recc.database.interfaces.db_daemon import DbDaemon
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.daemon import (
    INSERT_DAEMON,
    UPDATE_DAEMON_REQUIREMENTS_SHA256_BY_UID,
    DELETE_DAEMON_BY_UID,
    DELETE_DAEMON_BY_SLUG,
    SELECT_DAEMON_BY_UID,
    SELECT_DAEMON_UID_BY_SLUG,
    SELECT_DAEMON_ADDRESS_BY_SLUG,
    SELECT_DAEMON_BY_SLUG,
    SELECT_DAEMON_ALL,
    get_update_daemon_query_by_uid,
)


class PgDaemon(DbDaemon, PgBase):
    @overrides
    async def insert_daemon(
        self,
        plugin: str,
        slug: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        requirements_sha256: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        enable=False,
        created_at: Optional[datetime] = None,
    ) -> int:
        query = INSERT_DAEMON
        created = created_at if created_at else today()
        uid = await self.fetch_val(
            query,
            plugin,
            slug,
            name,
            address,
            requirements_sha256,
            description,
            extra,
            enable,
            created,
        )
        params_msg = f"plugin={plugin}"
        logger.info(f"insert_daemon({params_msg}) -> {uid}")
        return uid

    @overrides
    async def update_daemon_requirements_sha256_by_uid(
        self,
        uid: int,
        requirements_sha256: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_DAEMON_REQUIREMENTS_SHA256_BY_UID
        updated = updated_at if updated_at else today()
        await self.execute(query, uid, requirements_sha256, updated)
        params_msg = f"uid={uid}"
        logger.info(f"update_daemon_requirements_sha256_by_uid({params_msg}) ok.")

    @overrides
    async def update_daemon_by_uid(
        self,
        uid: int,
        plugin: Optional[str] = None,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        requirements_sha256: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        enable: Optional[bool] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query, args = get_update_daemon_query_by_uid(
            uid=uid,
            plugin=plugin,
            slug=slug,
            name=name,
            address=address,
            requirements_sha256=requirements_sha256,
            description=description,
            extra=extra,
            enable=enable,
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        params_msg = f"uid={uid}"
        logger.info(f"update_daemon_by_uid({params_msg}) ok.")

    @overrides
    async def delete_daemon_by_uid(self, uid: int) -> None:
        query = DELETE_DAEMON_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_daemon_by_uid({params_msg}) ok.")

    @overrides
    async def delete_daemon_by_slug(self, slug: str) -> None:
        query = DELETE_DAEMON_BY_SLUG
        await self.execute(query, slug)
        params_msg = f"slug={slug}"
        logger.info(f"delete_daemon_by_slug({params_msg}) ok.")

    @overrides
    async def select_daemon_by_uid(self, uid: int) -> Daemon:
        query = SELECT_DAEMON_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found daemon: {params_msg}")
        result = Daemon(**dict(row))
        logger.info(f"select_daemon_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_daemon_uid_by_slug(self, slug: str) -> int:
        query = SELECT_DAEMON_UID_BY_SLUG
        uid = await self.fetch_val(query, slug)
        params_msg = f"slug={slug}"
        if not isinstance(uid, int):
            raise RuntimeError(f"Not found daemon: {params_msg}")
        logger.info(f"select_daemon_uid_by_slug({params_msg}) -> {uid}")
        return uid

    @overrides
    async def select_daemon_address_by_slug(self, slug: str) -> str:
        query = SELECT_DAEMON_ADDRESS_BY_SLUG
        address = await self.fetch_val(query, slug)
        params_msg = f"slug={slug}"
        if not isinstance(address, str):
            raise RuntimeError(f"Not found daemon: {params_msg}")
        logger.info(f"select_daemon_address_by_slug({params_msg}) -> {address}")
        return address

    @overrides
    async def select_daemon_by_slug(self, slug: str) -> Daemon:
        query = SELECT_DAEMON_BY_SLUG
        row = await self.fetch_row(query, slug)
        params_msg = f"slug={slug}"
        if not row:
            raise RuntimeError(f"Not found daemon: {params_msg}")
        result = Daemon(**dict(row))
        logger.info(f"select_daemon_by_slug({params_msg}) ok.")
        return result

    @overrides
    async def select_daemons(self) -> List[Daemon]:
        result: List[Daemon] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_DAEMON_ALL
                async for row in conn.cursor(query):
                    result.append(Daemon(**dict(row)))
        result_msg = f"{len(result)} daemons"
        logger.info(f"select_daemons() -> {result_msg}")
        return result
