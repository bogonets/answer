# -*- coding: utf-8 -*-

from typing import Optional
from aioredis import Redis, ConnectionPool
from recc.cache.cache_store_interface import CacheStoreInterface
from recc.variables.cache import DEFAULT_MAX_CONNECTIONS

EX_KEY_MAX_CONNECTIONS = "max_connections"


class RedisCacheStore(CacheStoreInterface):
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
        self._redis: Optional[Redis] = None

    def _get_max_connections(self, default_value=DEFAULT_MAX_CONNECTIONS) -> int:
        try:
            return int(self._kwargs.get(EX_KEY_MAX_CONNECTIONS, default_value))
        except ValueError:
            return default_value

    def is_open(self) -> bool:
        return self._redis is not None

    async def open(self) -> None:
        pool = ConnectionPool.from_url(
            f"redis://{self._cs_host}:{self._cs_port}",
            password=self._cs_pw if self._cs_pw else None,
            max_connections=self._get_max_connections(),
        )
        self._redis = Redis(connection_pool=pool)

    async def close(self) -> None:
        assert self._redis
        await self._redis.close()
        self._redis = None

    async def set(self, key: str, val: bytes) -> None:
        assert self._redis
        await self._redis.execute_command("SET", key, val)

    async def get(self, key: str) -> bytes:
        assert self._redis
        result = await self._redis.execute_command("GET", key)
        assert isinstance(result, bytes)
        return result

    async def delete(self, key: str) -> None:
        assert self._redis
        await self._redis.execute_command("DEL", key)

    async def exists(self, key: str) -> bool:
        assert self._redis
        result = await self._redis.execute_command("EXISTS", key)
        assert isinstance(result, int)
        return bool(result)
