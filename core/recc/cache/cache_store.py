# -*- coding: utf-8 -*-

from typing import Optional
from recc.variables.cache import CS_TYPE_NAME_REDIS
from recc.cache.cache_store_interface import CacheStoreInterface
from recc.cache.redis.redis_cache_store import RedisCacheStore


def create_cache_store(
    cs_type: str,
    host: str,
    port: int,
    pw: Optional[str] = None,
    prefix: Optional[str] = None,
    **kwargs,
) -> CacheStoreInterface:
    if cs_type == CS_TYPE_NAME_REDIS:
        return RedisCacheStore(host, port, pw, prefix, **kwargs)
    else:
        raise ValueError(f"Unknown cache-store type: {cs_type}")
