# -*- coding: utf-8 -*-

from typing import Optional
from asyncpg.connection import Connection
from asyncpg.pool import Pool, PoolAcquireContext


class PgConnection:
    """
    Implementation for Type Hinting.
    """

    __slots__ = ("_pool", "_conn", "_timeout")

    def __init__(self, pool: Pool, timeout: Optional[float] = None):
        assert pool is not None
        self._pool = pool
        self._conn: Optional[PoolAcquireContext] = None
        self._timeout = timeout

    async def __aenter__(self) -> Connection:
        conn = await self._pool.acquire(timeout=self._timeout)
        self._conn = conn
        return self._conn

    async def __aexit__(self, exc_type, exc_value, tb):
        await self._pool.release(self._conn)
