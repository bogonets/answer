# -*- coding: utf-8 -*-

from typing import Optional, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import tznow
from recc.database.struct.port import Port, SockType
from recc.database.interfaces.db_port import DbPort
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.port import (
    INSERT_PORT,
    DELETE_PORT_BY_NUMBER_AND_SOCK,
    SELECT_PORT_BY_NUMBER,
    SELECT_PORT_ALL,
    get_update_port_query_by_number,
)


class PgPort(DbPort, PgBase):
    @overrides
    async def insert_port(
        self,
        number: int,
        sock: SockType,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        created = created_at if created_at else tznow()
        await self.execute(
            INSERT_PORT,
            number,
            sock.value,
            ref_uid,
            ref_category,
            created,
        )

    @overrides
    async def update_port_by_number(
        self,
        number: int,
        sock: SockType,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        query, args = get_update_port_query_by_number(
            number=number,
            sock=sock.value,
            ref_uid=ref_uid,
            ref_category=ref_category,
            updated_at=updated,
        )
        await self.execute(query, *args)

    @overrides
    async def delete_port_by_number_and_sock(self, number: int, sock: SockType) -> None:
        await self.execute(DELETE_PORT_BY_NUMBER_AND_SOCK, number, sock.value)

    @overrides
    async def select_port_by_number_and_sock(self, number: int, sock: SockType) -> Port:
        return await self.row(Port, SELECT_PORT_BY_NUMBER, number, sock.value)

    @overrides
    async def select_ports(self) -> List[Port]:
        return await self.rows(Port, SELECT_PORT_ALL)
