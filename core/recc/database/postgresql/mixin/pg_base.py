# -*- coding: utf-8 -*-

from typing import Optional, Any, Type, Iterable
from asyncpg import Record
from asyncpg.pool import Pool
from recc.database.postgresql.pg_connection import PgConnection


class PgBase:
    """
    Connection helper.
    """

    _pool: Optional[Pool]

    _host: Optional[str]
    _port: Optional[int]
    _user: Optional[str]
    _pw: Optional[str]
    _name: Optional[str]

    _timeout: float

    def conn(self, timeout: Optional[float] = None) -> PgConnection:
        assert self._pool is not None
        return PgConnection(self._pool, timeout=timeout)

    async def execute(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            await conn.execute(query, *args, timeout=timeout)

    async def executes(
        self,
        queries: Iterable[str],
        timeout: Optional[float] = None,
        isolation=None,
        readonly=False,
        deferrable=False,
    ) -> Any:
        async with self.conn(timeout) as conn:
            async with conn.transaction(
                isolation=isolation,
                readonly=readonly,
                deferrable=deferrable,
            ):
                for query in queries:
                    await conn.execute(query, timeout=timeout)

    async def fetch(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
        record_class: Optional[Type[Record]] = None,
    ) -> Any:
        async with self.conn() as conn:
            return await conn.fetch(
                query, *args, timeout=timeout, record_class=record_class
            )

    async def fetch_row(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
        record_class: Optional[Type[Record]] = None,
    ) -> Any:
        async with self.conn() as conn:
            return await conn.fetchrow(
                query, *args, timeout=timeout, record_class=record_class
            )

    async def fetch_val(
        self,
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)
