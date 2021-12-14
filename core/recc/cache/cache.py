# -*- coding: utf-8 -*-

from typing import Optional, Tuple
from recc.cache.cache_store_interface import CacheStoreInterface
from recc.cache.cache_store import create_cache_store
from recc.variables.cache import (
    CACHE_FORMAT_USER_NAME_TO_UID,
    CACHE_FORMAT_USER_UID_TO_NAME,
    CACHE_FORMAT_GROUP_SLUG_TO_UID,
    CACHE_FORMAT_GROUP_UID_TO_SLUG,
    CACHE_FORMAT_PROJECT_KEY_TO_UID,
    CACHE_FORMAT_PROJECT_UID_TO_KEY,
    CACHE_FORMAT_ROLE_SLUG_TO_UID,
    CACHE_FORMAT_ROLE_UID_TO_SLUG,
    PROJECT_KEY_SEPARATOR,
    PROJECT_KEY_FORMAT,
)


def key_user_name_to_uid(name: str) -> str:
    return CACHE_FORMAT_USER_NAME_TO_UID.format(name=name)


def key_user_uid_to_name(uid: int) -> str:
    return CACHE_FORMAT_USER_UID_TO_NAME.format(uid=uid)


def key_group_slug_to_uid(slug: str) -> str:
    return CACHE_FORMAT_GROUP_SLUG_TO_UID.format(slug=slug)


def key_group_uid_to_slug(uid: int) -> str:
    return CACHE_FORMAT_GROUP_UID_TO_SLUG.format(uid=uid)


def key_project(group_uid: int, project_slug: str) -> str:
    return PROJECT_KEY_FORMAT.format(group_uid=group_uid, project_slug=project_slug)


def key_project_key_to_uid(project_key: str) -> str:
    return CACHE_FORMAT_PROJECT_KEY_TO_UID.format(key=project_key)


def key_project_uid_to_key(project_uid: int) -> str:
    return CACHE_FORMAT_PROJECT_UID_TO_KEY.format(uid=project_uid)


def key_role_slug_to_uid(slug: str) -> str:
    return CACHE_FORMAT_ROLE_SLUG_TO_UID.format(slug=slug)


def key_role_uid_to_slug(uid: int) -> str:
    return CACHE_FORMAT_ROLE_UID_TO_SLUG.format(uid=uid)


class Cache:
    def __init__(
        self,
        cs_type: str,
        host: str,
        port: int,
        pw: Optional[str] = None,
        prefix: Optional[str] = None,
        **kwargs,
    ):
        self._store = create_cache_store(cs_type, host, port, pw, prefix, **kwargs)

    def is_open(self) -> bool:
        return self._store.is_open()

    async def open(self) -> None:
        await self._store.open()

    async def close(self) -> None:
        await self._store.close()

    @property
    def store(self) -> CacheStoreInterface:
        assert self._store is not None
        assert self._store.is_open()
        return self._store

    async def clear(self) -> None:
        await self.store.clear()

    async def get_str(self, key: str, encoding="utf-8") -> Optional[str]:
        val = await self.store.get(key)
        return str(val, encoding=encoding) if val else None

    async def get_int(self, key: str) -> Optional[int]:
        val = await self.store.get(key)
        return int(val) if val else None

    async def get_float(self, key: str) -> Optional[float]:
        val = await self.store.get(key)
        return float(val) if val else None

    # -----------------
    # user name <-> uid
    # -----------------

    async def get_user_uid(self, name: str) -> Optional[int]:
        return await self.get_int(key_user_name_to_uid(name))

    async def get_user_name(self, uid: int) -> Optional[str]:
        return await self.get_str(key_user_uid_to_name(uid))

    async def set_user(self, name: str, uid: int) -> None:
        name_to_uid = key_user_name_to_uid(name)
        uid_to_name = key_user_uid_to_name(uid)
        await self.store.mset({name_to_uid: uid, uid_to_name: name})

    async def remove_user_by_uid(self, uid: int) -> None:
        uid_to_name = key_user_uid_to_name(uid)
        name = await self.get_str(uid_to_name)
        if name is not None:
            name_to_uid = key_user_name_to_uid(name)
            await self.store.delete(uid_to_name, name_to_uid)
        else:
            await self.store.delete(uid_to_name)

    # ------------------
    # group slug <-> uid
    # ------------------

    async def get_group_uid(self, slug: str) -> Optional[int]:
        return await self.get_int(key_group_slug_to_uid(slug))

    async def get_group_slug(self, uid: int) -> Optional[str]:
        return await self.get_str(key_group_uid_to_slug(uid))

    async def set_group(self, slug: str, uid: int) -> None:
        slug_to_uid = key_group_slug_to_uid(slug)
        uid_to_slug = key_group_uid_to_slug(uid)
        await self.store.mset({slug_to_uid: uid, uid_to_slug: slug})

    async def remove_group_by_uid(self, uid: int) -> None:
        uid_to_slug = key_group_uid_to_slug(uid)
        slug = await self.get_str(uid_to_slug)
        if slug is not None:
            slug_to_uid = key_group_slug_to_uid(slug)
            await self.store.delete(uid_to_slug, slug_to_uid)
        else:
            await self.store.delete(uid_to_slug)

    # --------------------
    # project slug <-> uid
    # --------------------

    async def get_project_uid(self, group_uid: int, project_slug: str) -> Optional[int]:
        project_key = key_project(group_uid, project_slug)
        return await self.get_int(key_project_key_to_uid(project_key))

    async def get_project_key(self, project_uid: int) -> Optional[Tuple[int, str]]:
        uid_to_key = key_project_uid_to_key(project_uid)
        val = await self.get_str(uid_to_key)
        if val is None:
            return None
        project_keys = val.split(PROJECT_KEY_SEPARATOR)
        assert len(project_keys) == 2
        group_uid = int(project_keys[0])
        project_slug = project_keys[1]
        return group_uid, project_slug

    async def set_project(
        self, group_uid: int, project_slug: str, project_uid: int
    ) -> None:
        project_key = key_project(group_uid, project_slug)
        key_to_uid = key_project_key_to_uid(project_key)
        uid_to_key = key_project_uid_to_key(project_uid)
        await self._store.mset({key_to_uid: project_uid, uid_to_key: project_key})

    async def remove_project_by_uid(self, project_uid: int) -> None:
        uid_to_key = key_project_uid_to_key(project_uid)
        project_key = await self.get_str(uid_to_key)
        if project_key is not None:
            key_to_uid = key_project_key_to_uid(project_key)
            await self._store.delete(uid_to_key, key_to_uid)
        else:
            await self._store.delete(uid_to_key)

    # -----------------
    # role slug <-> uid
    # -----------------

    async def get_role_uid(self, slug: str) -> Optional[int]:
        return await self.get_int(key_role_slug_to_uid(slug))

    async def get_role_slug(self, uid: int) -> Optional[str]:
        return await self.get_str(key_role_uid_to_slug(uid))

    async def set_role(self, slug: str, uid: int) -> None:
        slug_to_uid = key_role_slug_to_uid(slug)
        uid_to_slug = key_role_uid_to_slug(uid)
        await self._store.mset({slug_to_uid: uid, uid_to_slug: slug})

    async def remove_role_by_uid(self, uid: int) -> None:
        uid_to_slug = key_role_uid_to_slug(uid)
        slug = await self.get_str(uid_to_slug)
        if slug is not None:
            slug_to_uid = key_role_slug_to_uid(slug)
            await self._store.delete(uid_to_slug, slug_to_uid)
        else:
            await self._store.delete(uid_to_slug)
