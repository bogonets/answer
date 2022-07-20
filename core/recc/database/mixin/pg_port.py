# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.port import (
    DELETE_PORT_BY_NUMBER_AND_SOCK,
    INSERT_PORT,
    SELECT_PORT_ALL,
    SELECT_PORT_BY_NUMBER,
    SELECT_PORT_BY_REF_UID_AND_REF_CATEGORY,
    SELECT_PORT_NUMBER_ALL,
    get_update_port_query_by_number,
)
from recc.packet.port import Port, SockType


class PgPort(PgBase):
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

    async def delete_port_by_number_and_sock(self, number: int, sock: SockType) -> None:
        await self.execute(DELETE_PORT_BY_NUMBER_AND_SOCK, number, sock.value)

    async def select_port_by_number_and_sock(self, number: int, sock: SockType) -> Port:
        return await self.row(Port, SELECT_PORT_BY_NUMBER, number, sock.value)

    async def select_port_all(self) -> List[Port]:
        return await self.rows(Port, SELECT_PORT_ALL)

    async def select_port_by_ref_uid_and_ref_category(
        self, ref_uid: int, ref_category: str
    ) -> List[Port]:
        return await self.rows(
            Port,
            SELECT_PORT_BY_REF_UID_AND_REF_CATEGORY,
            ref_uid,
            ref_category,
        )

    async def select_port_number_all(self) -> List[int]:
        rows = await self.fetch_rows(SELECT_PORT_NUMBER_ALL)
        return [row["number"] for row in rows]
