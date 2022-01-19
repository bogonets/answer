# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.database.struct.port import Port
from recc.database.interfaces.db_port import DbPort
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.port import (
    INSERT_PORT,
    UPDATE_PORT_DESCRIPTION_BY_NUMBER,
    UPDATE_PORT_EXTRA_BY_NUMBER,
    DELETE_PORT_BY_NUMBER,
    SELECT_PORT_BY_NUMBER,
    SELECT_PORT_ALL,
    get_update_port_query_by_number,
)


class PgPort(DbPort, PgBase):
    @overrides
    async def insert_port(
        self,
        number: int,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        created = created_at if created_at else today()
        await self.execute(
            INSERT_PORT,
            number,
            ref_uid,
            ref_category,
            description,
            extra,
            created,
        )

    @overrides
    async def update_port_description_by_number(
        self,
        number: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(
            UPDATE_PORT_DESCRIPTION_BY_NUMBER,
            number,
            description,
            updated,
        )

    @overrides
    async def update_port_extra_by_number(
        self,
        number: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(UPDATE_PORT_EXTRA_BY_NUMBER, number, extra, updated)

    @overrides
    async def update_port_by_number(
        self,
        number: int,
        ref_uid: Optional[int] = None,
        ref_category: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        query, args = get_update_port_query_by_number(
            number=number,
            ref_uid=ref_uid,
            ref_category=ref_category,
            description=description,
            extra=extra,
            updated_at=updated,
        )
        await self.execute(query, *args)

    @overrides
    async def delete_port_by_number(self, number: int) -> None:
        await self.execute(DELETE_PORT_BY_NUMBER, number)

    @overrides
    async def select_port_by_number(self, number: int) -> Port:
        return await self.row(Port, SELECT_PORT_BY_NUMBER, number)

    @overrides
    async def select_ports(self) -> List[Port]:
        return await self.rows(Port, SELECT_PORT_ALL)
