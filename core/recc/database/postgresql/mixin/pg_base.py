# -*- coding: utf-8 -*-

from typing import Optional, Any, Type
from asyncpg import Record
from asyncpg.connection import Connection
from asyncpg.pool import Pool, PoolAcquireContext


class PgBase:
    """
    Connection helper.
    """

    _pool: Optional[Pool]

    _db_host: Optional[str]
    _db_port: Optional[int]
    _db_user: Optional[str]
    _db_pw: Optional[str]
    _db_name: Optional[str]

    _timeout: float

    _anonymous_group_uid: Optional[int]
    _guest_permission_uid: Optional[int]
    _reporter_permission_uid: Optional[int]
    _operator_permission_uid: Optional[int]
    _maintainer_permission_uid: Optional[int]

    class _Connection:
        """
        Implementation for Type Hinting.
        """

        __slots__ = ("_pool", "_conn")

        def __init__(self, pool: Pool):
            self._pool = pool
            self._conn: Optional[PoolAcquireContext] = None
            assert self._pool is not None

        async def __aenter__(self) -> Connection:
            conn = await self._pool.acquire()
            self._conn = conn
            return self._conn

        async def __aexit__(self, exc_type, exc_value, tb):
            await self._pool.release(self._conn)

    def conn(self) -> _Connection:
        assert self._pool is not None
        return self._Connection(self._pool)

    async def execute(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            await conn.execute(query, *args, timeout=timeout)

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

    async def fetch_val(
        self,
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)

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
