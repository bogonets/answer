# -*- coding: utf-8 -*-

from typing import Optional
from recc.variables.cache import CS_TYPE_NAME_REDIS
from recc.cache.async_cs_interface import AsyncCacheStoreInterface
from recc.cache.redis.async_redis import AsyncRedisCacheStore


def create_cache_store(
    cs_type: str,
    cs_host: str,
    cs_port: int,
    cs_pw: Optional[str] = None,
    **kwargs,
) -> AsyncCacheStoreInterface:
    if cs_type == CS_TYPE_NAME_REDIS:
        return AsyncRedisCacheStore(cs_host, cs_port, cs_pw, **kwargs)
    else:
        raise ValueError(f"Unknown cache-store type: {cs_type}")
