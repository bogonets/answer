# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.create.functions.add_daemon_and_port import (
    get_insert_daemon_and_port,
)
from recc.database.query.daemon import (
    DELETE_DAEMON_BY_SLUG,
    DELETE_DAEMON_BY_UID,
    SELECT_DAEMON_ADDRESS_BY_SLUG,
    SELECT_DAEMON_ALL,
    SELECT_DAEMON_BY_SLUG,
    SELECT_DAEMON_BY_UID,
    SELECT_DAEMON_UID_BY_SLUG,
    get_update_daemon_query_by_uid,
)
from recc.packet.daemon import Daemon
from recc.uri.rpc_uri import parse_rpc_address_as_class


class PgDaemon(PgBase):
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
        tcp_ports: List[int] = list()
        if address:
            rpc_address = parse_rpc_address_as_class(address)
            if rpc_address.has_any_port:
                tcp_ports = rpc_address.all_ports
        query = get_insert_daemon_and_port(
            d_plugin=plugin,
            d_slug=slug,
            d_name=name if name else str(),
            d_address=address if address else str(),
            d_description=description if description else str(),
            d_enable=enable,
            d_created=created,
            p_tcp_ports=tcp_ports,
        )
        return await self.column(int, query)

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

    async def delete_daemon_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_DAEMON_BY_UID, uid)

    async def delete_daemon_by_slug(self, slug: str) -> None:
        await self.execute(DELETE_DAEMON_BY_SLUG, slug)

    async def select_daemon_by_uid(self, uid: int) -> Daemon:
        return await self.row(Daemon, SELECT_DAEMON_BY_UID, uid)

    async def select_daemon_by_slug(self, slug: str) -> Daemon:
        return await self.row(Daemon, SELECT_DAEMON_BY_SLUG, slug)

    async def select_daemon_uid_by_slug(self, slug: str) -> int:
        return await self.column(int, SELECT_DAEMON_UID_BY_SLUG, slug)

    async def select_daemon_address_by_slug(self, slug: str) -> str:
        return await self.column(str, SELECT_DAEMON_ADDRESS_BY_SLUG, slug)

    async def select_daemons(self) -> List[Daemon]:
        return await self.rows(Daemon, SELECT_DAEMON_ALL)
