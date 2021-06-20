# -*- coding: utf-8 -*-

from typing import Optional
from aioredis import create_pool, ConnectionsPool, RedisConnection
from aioredis.abc import AbcPool
from recc.cache.async_cs_interface import AsyncCacheStoreInterface
from recc.variables.cache import (
    DEFAULT_CONNECTION_POOL_MIN_SIZE,
    DEFAULT_CONNECTION_POOL_MAX_SIZE,
)

EX_KEY_MINSIZE = "minsize"
EX_KEY_MAXSIZE = "maxsize"


class AsyncRedisCacheStore(AsyncCacheStoreInterface):
    """
    Redis cache store class.
    """

    def __init__(
        self,
        cs_host: str,
        cs_port: int,
        cs_pw: Optional[str] = None,
        **kwargs,
    ):
        self._cs_host = cs_host
        self._cs_port = cs_port
        self._cs_pw = cs_pw
        self._kwargs = kwargs
        self._pool: Optional[ConnectionsPool] = None

    def _get_minsize(self, default_value=DEFAULT_CONNECTION_POOL_MIN_SIZE) -> int:
        try:
            return int(self._kwargs.get(EX_KEY_MINSIZE, default_value))
        except ValueError:
            return default_value

    def _get_maxsize(self, default_value=DEFAULT_CONNECTION_POOL_MAX_SIZE) -> int:
        try:
            return int(self._kwargs.get(EX_KEY_MAXSIZE, default_value))
        except ValueError:
            return default_value

    def is_open(self) -> bool:
        return self._pool is not None

    async def open(self) -> None:
        self._pool = await create_pool(
            address=f"redis://{self._cs_host}:{self._cs_port}",
            password=self._cs_pw if self._cs_pw else None,
            minsize=self._get_minsize(),
            maxsize=self._get_maxsize(),
        )

    async def close(self) -> None:
        assert self._pool
        self._pool.close()
        await self._pool.wait_closed()
        self._pool = None

    @property
    def pool(self) -> ConnectionsPool:
        assert self._pool
        return self._pool

    class _Connection:
        """
        Implementation for Type Hinting.
        """

        __slots__ = ("_pool", "_conn")

        def __init__(self, pool: AbcPool):
            self._pool = pool
            self._conn: Optional[RedisConnection] = None

        async def __aenter__(self) -> RedisConnection:
            conn = await self._pool.acquire()
            self._conn = conn
            return self._conn

        async def __aexit__(self, exc_type, exc_value, tb):
            try:
                self._pool.release(self._conn)
            finally:
                self._pool = None
                self._conn = None

    def _conn(self) -> _Connection:
        return self._Connection(self.pool)

    async def set(self, key: str, val: bytes) -> None:
        async with self._conn() as conn:
            await conn.execute(b"SET", key, val)

    async def get(self, key: str) -> bytes:
        async with self._conn() as conn:
            return await conn.execute(b"GET", key)

    async def delete(self, key: str) -> None:
        async with self._conn() as conn:
            await conn.execute(b"DEL", key)

    async def exists(self, key: str) -> bool:
        async with self._conn() as conn:
            return bool(await conn.execute(b"EXISTS", key))
