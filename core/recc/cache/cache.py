# -*- coding: utf-8 -*-

from threading import Lock
from typing import Optional, Dict, Tuple
from recc.cache.cache_store import create_cache_store

ProjectKey = Tuple[int, str]


class Cache:
    def __init__(
        self,
        cs_type: str,
        cs_host: str,
        cs_port: int,
        cs_pw: Optional[str] = None,
        **kwargs,
    ):
        self._store = create_cache_store(cs_type, cs_host, cs_port, cs_pw, **kwargs)

        # User
        self._user_lock = Lock()
        self._username_to_uid: Dict[str, int] = dict()
        self._uid_to_username: Dict[int, str] = dict()

        # Group
        self._group_lock = Lock()
        self._group_slug_to_uid: Dict[str, int] = dict()
        self._group_uid_to_slug: Dict[int, str] = dict()

        # Project
        self._project_lock = Lock()
        self._project_uid_to_slug: Dict[int, str] = dict()
        self._project_uid_to_group_uid: Dict[int, int] = dict()
        self._project_key_to_project_uid: Dict[ProjectKey, int] = dict()

        # Permission
        self._permission_lock = Lock()
        self._permission_name_to_uid: Dict[str, int] = dict()
        self._permission_uid_to_name: Dict[int, str] = dict()

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

    def exists_username(self, username: str) -> bool:
        with self._user_lock:
            return username in self._username_to_uid

    def exists_user_uid(self, user_uid: int) -> bool:
        with self._user_lock:
            return user_uid in self._uid_to_username

    def get_user_uid(self, username: str) -> Optional[int]:
        with self._user_lock:
            return self._username_to_uid.get(username, None)

    def get_username(self, user_uid: int) -> Optional[str]:
        with self._user_lock:
            return self._uid_to_username.get(user_uid, None)

    def set_user(self, username: str, user_uid: int) -> None:
        with self._user_lock:
            self._username_to_uid[username] = user_uid
            self._uid_to_username[user_uid] = username

    # -----------------
    # group slug -> uid
    # -----------------

    def exists_group_slug(self, group_slug: str) -> bool:
        with self._group_lock:
            return group_slug in self._group_slug_to_uid

    def exists_group_uid(self, group_uid: int) -> bool:
        with self._group_lock:
            return group_uid in self._group_uid_to_slug

    def get_group_uid(self, group_slug: str) -> Optional[int]:
        with self._group_lock:
            return self._group_slug_to_uid.get(group_slug, None)

    def get_group_slug(self, group_uid: int) -> Optional[str]:
        with self._group_lock:
            return self._group_uid_to_slug.get(group_uid, None)

    def set_group(self, group_uid: int, group_slug: str) -> None:
        with self._group_lock:
            self._group_slug_to_uid[group_slug] = group_uid
            self._group_uid_to_slug[group_uid] = group_slug

    # -------------------
    # project slug -> uid
    # -------------------

    def exists_project_uid(self, project_uid: int) -> bool:
        with self._project_lock:
            return project_uid in self._project_uid_to_group_uid

    def exists_group_uid_and_project_slug(
        self, group_uid: int, project_slug: str
    ) -> bool:
        with self._project_lock:
            key = (group_uid, project_slug)
            return key in self._project_key_to_project_uid

    def get_group_uid_by_project_uid(self, project_uid: int) -> Optional[int]:
        with self._project_lock:
            return self._project_uid_to_group_uid.get(project_uid, None)

    def get_project_slug(self, project_uid: int) -> Optional[str]:
        with self._project_lock:
            return self._project_uid_to_slug.get(project_uid, None)

    def get_project_uid(self, group_uid: int, project_slug: str) -> Optional[int]:
        with self._project_lock:
            key = (group_uid, project_slug)
            return self._project_key_to_project_uid.get(key, None)

    def set_project(self, project_uid: int, group_uid: int, project_slug: str) -> None:
        with self._project_lock:
            self._project_uid_to_slug[project_uid] = project_slug
            self._project_uid_to_group_uid[project_uid] = group_uid

            key = (group_uid, project_slug)
            self._project_key_to_project_uid[key] = project_uid

    # ----------------------
    # permission name -> uid
    # ----------------------

    def exists_permission_name(self, name: str) -> bool:
        with self._permission_lock:
            return name in self._permission_name_to_uid

    def exists_permission_uid(self, uid: int) -> bool:
        with self._permission_lock:
            return uid in self._permission_uid_to_name

    def get_permission_uid(self, name: str) -> Optional[int]:
        with self._permission_lock:
            return self._permission_name_to_uid.get(name, None)

    def get_permission_name(self, uid: int) -> Optional[str]:
        with self._permission_lock:
            return self._permission_uid_to_name.get(uid, None)

    def set_permission(self, uid: int, name: str) -> None:
        with self._permission_lock:
            self._permission_name_to_uid[name] = uid
            self._permission_uid_to_name[uid] = name
