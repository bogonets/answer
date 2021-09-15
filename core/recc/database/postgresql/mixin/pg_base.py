# -*- coding: utf-8 -*-

from typing import Optional, Any, Type, Iterable
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
    _owner_permission_uid: Optional[int]

    class _Connection:
        """
        Implementation for Type Hinting.
        """

        __slots__ = ("_pool", "_conn", "_timeout")

        def __init__(self, pool: Pool, timeout: Optional[float] = None):
            self._pool = pool
            self._conn: Optional[PoolAcquireContext] = None
            self._timeout = timeout
            assert self._pool is not None

        async def __aenter__(self) -> Connection:
            conn = await self._pool.acquire(timeout=self._timeout)
            self._conn = conn
            return self._conn

        async def __aexit__(self, exc_type, exc_value, tb):
            await self._pool.release(self._conn)

    def conn(self, timeout: Optional[float] = None) -> _Connection:
        assert self._pool is not None
        return self._Connection(self._pool, timeout=timeout)

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
