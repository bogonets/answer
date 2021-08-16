# -*- coding: utf-8 -*-

from typing import Optional, Dict
from recc.cache.cache_store_interface import CacheStoreInterface
from recc.cache.cache_store import create_cache_store


class Cache:

    _store: CacheStoreInterface

    # User
    _username_to_uid: Dict[str, int]
    _uid_to_username: Dict[int, str]

    # Group
    _group_slug_to_uid: Dict[str, int]
    _group_uid_to_slug: Dict[int, str]

    def __init__(
        self,
        cs_type: str,
        cs_host: str,
        cs_port: int,
        cs_pw: Optional[str] = None,
        **kwargs,
    ):
        self._store = create_cache_store(cs_type, cs_host, cs_port, cs_pw, **kwargs)

    # ------------
    # Store bypass
    # ------------

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

    # ---------------
    # username -> uid
    # ---------------

    @property
    def username_to_uid(self):
        return self._username_to_uid

    @property
    def uid_to_username(self):
        return self._uid_to_username

    def exists_username(self, username: str) -> bool:
        return username in self._username_to_uid

    def exists_user_uid(self, user_uid: int) -> bool:
        return user_uid in self._uid_to_username

    def get_user_uid(self, username: str) -> Optional[int]:
        return self._username_to_uid.get(username)

    def get_username(self, user_uid: int) -> Optional[str]:
        return self._uid_to_username.get(user_uid)

    def set_user(self, username: str, user_uid: int) -> None:
        self._username_to_uid[username] = user_uid
        self._uid_to_username[user_uid] = username

    # -----------------
    # group slug -> uid
    # -----------------

    @property
    def group_slug_to_uid(self):
        return self._group_slug_to_uid

    @property
    def group_uid_to_slug(self):
        return self._group_uid_to_slug

    def exists_group_slug(self, group_slug: str) -> bool:
        return group_slug in self._group_slug_to_uid

    def exists_group_uid(self, group_uid: int) -> bool:
        return group_uid in self._group_uid_to_slug

    def get_group_uid(self, group_slug: str) -> Optional[int]:
        return self._group_slug_to_uid.get(group_slug)

    def get_group_slug(self, group_uid: int) -> Optional[str]:
        return self._group_uid_to_slug.get(group_uid)

    def set_group(self, group_uid: int, group_slug: str) -> None:
        self._group_slug_to_uid[group_slug] = group_uid
        self._group_uid_to_slug[group_uid] = group_slug
