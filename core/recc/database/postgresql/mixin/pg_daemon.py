# -*- coding: utf-8 -*-

from typing import Optional, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import tznow
from recc.database.struct.daemon import Daemon
from recc.database.interfaces.db_daemon import DbDaemon
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.daemon import (
    INSERT_DAEMON,
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
        description: Optional[str] = None,
        enable=False,
        created_at: Optional[datetime] = None,
    ) -> int:
        created = created_at if created_at else tznow()
        return await self.column(
            int,
            INSERT_DAEMON,
            plugin,
            slug,
            name,
            address,
            description,
            enable,
            created,
        )

    @overrides
    async def update_daemon_by_uid(
        self,
        uid: int,
        plugin: Optional[str] = None,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        enable: Optional[bool] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query, args = get_update_daemon_query_by_uid(
            uid=uid,
            plugin=plugin,
            slug=slug,
            name=name,
            address=address,
            description=description,
            enable=enable,
            updated_at=updated_at,
        )
        await self.execute(query, *args)

    @overrides
    async def delete_daemon_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_DAEMON_BY_UID, uid)

    @overrides
    async def delete_daemon_by_slug(self, slug: str) -> None:
        await self.execute(DELETE_DAEMON_BY_SLUG, slug)

    @overrides
    async def select_daemon_by_uid(self, uid: int) -> Daemon:
        return await self.row(Daemon, SELECT_DAEMON_BY_UID, uid)

    @overrides
    async def select_daemon_by_slug(self, slug: str) -> Daemon:
        return await self.row(Daemon, SELECT_DAEMON_BY_SLUG, slug)

    @overrides
    async def select_daemon_uid_by_slug(self, slug: str) -> int:
        return await self.column(int, SELECT_DAEMON_UID_BY_SLUG, slug)

    @overrides
    async def select_daemon_address_by_slug(self, slug: str) -> str:
        return await self.column(str, SELECT_DAEMON_ADDRESS_BY_SLUG, slug)

    @overrides
    async def select_daemons(self) -> List[Daemon]:
        return await self.rows(Daemon, SELECT_DAEMON_ALL)
