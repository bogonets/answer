# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.port import Port
from recc.database.interfaces.db_port import DbPort
from recc.database.postgresql.mixin.pg_base import PgBase
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
        query = INSERT_PORT
        created = created_at if created_at else today()
        await self.execute(
            query,
            number,
            ref_uid,
            ref_category,
            description,
            extra,
            created,
        )
        params_msg = f"number={number}"
        logger.info(f"insert_port({params_msg}) ok.")

    @overrides
    async def update_port_description_by_number(
        self,
        number: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_PORT_DESCRIPTION_BY_NUMBER
        updated = updated_at if updated_at else today()
        await self.execute(query, number, description, updated)
        params_msg = f"number={number}"
        logger.info(f"update_port_description_by_number({params_msg}) ok.")

    @overrides
    async def update_port_extra_by_number(
        self,
        number: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        query = UPDATE_PORT_EXTRA_BY_NUMBER
        updated = updated_at if updated_at else today()
        await self.execute(query, number, extra, updated)
        params_msg = f"number={number}"
        logger.info(f"update_port_extra_by_number({params_msg}) ok.")

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
        params_msg = f"number={number}"
        logger.info(f"update_port_by_number({params_msg}) ok.")

    @overrides
    async def delete_port_by_number(self, number: int) -> None:
        query = DELETE_PORT_BY_NUMBER
        await self.execute(query, number)
        params_msg = f"number={number}"
        logger.info(f"delete_port_by_number({params_msg}) ok.")

    @overrides
    async def select_port_by_number(self, number: int) -> Port:
        query = SELECT_PORT_BY_NUMBER
        row = await self.fetch_row(query, number)
        params_msg = f"number={number}"
        if not row:
            raise RuntimeError(f"Not found widget: {params_msg}")
        assert len(row) == 7
        result = Port(**dict(row))
        result.number = number
        logger.info(f"select_port_by_number({params_msg}) ok.")
        return result

    @overrides
    async def select_ports(self) -> List[Port]:
        result: List[Port] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_PORT_ALL
                async for row in conn.cursor(query):
                    result.append(Port(**dict(row)))
        result_msg = f"{len(result)} port"
        logger.info(f"select_ports() -> {result_msg}")
        return result
