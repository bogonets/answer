# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop

from recc_cache import Cache
from recc_database.database.pg_db import PgDb

from recc.config import Config
from recc.plugin.core_plugin_manager import CorePluginManager
from recc.session.session import SessionPairFactory


class ContextBase:

    _loop: AbstractEventLoop
    _config: Config
    _signature: str
    _session_factory: SessionPairFactory
    _cache: Cache
    _database: PgDb
    _plugins: CorePluginManager

    @property
    def config(self) -> Config:
        """
        Initialize parameters.
        """
        return self._config

    @property
    def loop(self) -> AbstractEventLoop:
        """
        Default event loop.
        """
        return self._loop

    @property
    def cache(self):
        """
        Cache Store property.
        """
        assert self._cache is not None
        if not self._cache.is_open():
            raise ValueError("The cache-store is not open")
        return self._cache

    def is_cache_open(self) -> bool:
        assert self._cache is not None
        return self._cache.is_open()

    @property
    def database(self):
        """
        Database property.
        """
        assert self._database is not None
        if not self._database.is_open():
            raise ValueError("The database is not open")
        return self._database

    def is_database_open(self) -> bool:
        assert self._database is not None
        return self._database.is_open()

    # ----------------
    # Database caching
    # ----------------

    _initialized_database = False

    async def is_initialized_database(self) -> bool:
        # After being created in the DB, there is no scenario that can be removed.
        if self._initialized_database:
            return True
        self._initialized_database = await self.database.select_exists_admin_user()
        return self._initialized_database

    async def get_user_uid(self, username: str, caching=True) -> int:
        if not username:
            raise ValueError("The `username` argument is empty.")

        uid = await self.cache.get_user_uid(username)
        if uid is None:
            try:
                uid = await self.database.select_user_uid_by_username(username)
                if caching:
                    await self.cache.set_user(username, uid)
            except RuntimeError:
                pass
        return uid

    async def get_user_name(self, user_uid: int, caching=True) -> str:
        username = await self.cache.get_user_name(user_uid)
        if username is None:
            try:
                username = await self.database.select_user_username_by_uid(user_uid)
                if caching:
                    await self.cache.set_user(username, user_uid)
            except RuntimeError:
                pass
        return username

    async def get_group_uid(self, group_slug: str, caching=True) -> int:
        if not group_slug:
            raise ValueError("The `group_slug` argument is empty.")

        uid = await self.cache.get_group_uid(group_slug)
        if uid is None:
            try:
                uid = await self.database.select_group_uid_by_slug(group_slug)
                if caching:
                    await self.cache.set_group(group_slug, uid)
            except RuntimeError:
                pass
        return uid

    async def get_group_slug(self, group_uid: int, caching=True) -> str:
        slug = await self.cache.get_group_slug(group_uid)
        if slug is None:
            try:
                slug = await self.database.select_group_slug_by_uid(group_uid)
                if caching:
                    await self.cache.set_group(slug, group_uid)
            except RuntimeError:
                pass
        return slug

    async def get_project_uid(
        self, group_uid: int, project_slug: str, caching=True
    ) -> int:
        if not project_slug:
            raise ValueError("The `project_slug` argument is empty.")

        uid = await self.cache.get_project_uid(group_uid, project_slug)
        if uid is None:
            try:
                uid = await self.database.select_project_uid_by_group_uid_and_slug(
                    group_uid, project_slug
                )
                if caching:
                    await self.cache.set_project(group_uid, project_slug, uid)
            except RuntimeError:
                pass
        return uid

    async def get_role_uid(self, role_slug: str, caching=True) -> int:
        if not role_slug:
            raise ValueError("The `role_slug` argument is empty.")

        uid = await self.cache.get_role_uid(role_slug)
        if uid is None:
            try:
                uid = await self.database.select_role_uid_by_slug(role_slug)
                if caching:
                    await self.cache.set_role(role_slug, uid)
            except RuntimeError:
                pass
        return uid

    async def get_role_slug(self, role_uid: int, caching=True) -> str:
        slug = await self.cache.get_role_slug(role_uid)
        if slug is None:
            try:
                slug = await self.database.select_role_slug_by_uid(role_uid)
                if caching:
                    await self.cache.set_role(slug, role_uid)
            except RuntimeError:
                pass
        return slug
