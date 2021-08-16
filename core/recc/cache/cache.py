# -*- coding: utf-8 -*-

from typing import Optional
from recc.cache.cache_store_interface import CacheStoreInterface
from recc.cache.cache_store import create_cache_store


class Cache:

    _store: CacheStoreInterface

    def __init__(
        self,
        cs_type: str,
        cs_host: str,
        cs_port: int,
        cs_pw: Optional[str] = None,
        **kwargs,
    ):
        self._store = create_cache_store(cs_type, cs_host, cs_port, cs_pw, **kwargs)

    def is_open(self) -> bool:
        return self._store.is_open()

    async def open(self) -> None:
        await self._store.open()

    async def close(self) -> None:
        await self._store.close()

    async def store_set(self, key: str, val: bytes) -> None:
        await self._store.set(key, val)

    async def store_get(self, key: str) -> bytes:
        return await self._store.get(key)

    async def store_delete(self, key: str) -> None:
        await self._store.delete(key)

    async def store_exists(self, key: str) -> bool:
        return await self._store.exists(key)
