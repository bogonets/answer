# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop
from recc.argparse.config.core_config import CoreConfig
from recc.session.session import SessionPairFactory
from recc.storage.core_storage import CoreStorage
from recc.container.interfaces.container_interface import ContainerInterface
from recc.cache.cache import Cache
from recc.database.interfaces.db_interface import DbInterface
from recc.task.task_connection_pool import TaskConnectionPool
from recc.resource.port_manager import PortManager
from recc.template.manager.lamda_template_manager import LamdaTemplateManager


class ContextBase:

    _loop: AbstractEventLoop
    _config: CoreConfig
    _signature: str
    _storage: CoreStorage
    _session_factory: SessionPairFactory
    _container: ContainerInterface
    _container_key: str
    _cache: Cache
    _database: DbInterface
    _tasks: TaskConnectionPool
    _ports: PortManager
    _templates: LamdaTemplateManager

    @property
    def config(self) -> CoreConfig:
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
    def storage(self):
        """
        Storage Manager property.
        """
        return self._storage

    @property
    def session_factory(self):
        """
        Session Factory property.
        """
        assert self._session_factory is not None
        return self._session_factory

    @property
    def container(self):
        """
        Container Manager property.
        """
        assert self._container is not None
        if not self._container.is_open():
            raise ValueError("The container-manager is not open")
        return self._container

    def is_container_open(self) -> bool:
        assert self._container is not None
        return self._container.is_open()

    def is_host_mode(self) -> bool:
        return len(self._container_key) == 0

    def is_guest_mode(self) -> bool:
        return not self.is_host_mode()

    @property
    def container_key(self) -> str:
        return self._container_key

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

    async def get_database_version(self) -> str:
        return await self.database.select_database_version()

    @property
    def tasks(self):
        """
        Task Manager.
        """
        assert self._tasks is not None
        return self._tasks

    @property
    def ports(self):
        """
        Port Manager.
        """
        assert self._ports is not None
        return self._ports

    # ----------------
    # Database caching
    # ----------------

    async def get_user_uid(self, username: str, caching=True) -> int:
        if not username:
            raise ValueError("The `username` argument is empty.")

        uid = self.cache.get_user_uid(username)
        if uid is None:
            try:
                uid = await self.database.select_user_uid_by_username(username)
                if caching:
                    self.cache.set_user(username, uid)
            except RuntimeError:
                pass
        return uid

    async def get_username(self, user_uid: int, caching=True) -> str:
        username = self.cache.get_username(user_uid)
        if username is None:
            try:
                username = await self.database.select_user_username_by_uid(user_uid)
                if caching:
                    self.cache.set_user(username, user_uid)
            except RuntimeError:
                pass
        return username

    async def get_group_uid(self, group_slug: str, caching=True) -> int:
        if not group_slug:
            raise ValueError("The `group_slug` argument is empty.")

        uid = self.cache.get_group_uid(group_slug)
        if uid is None:
            try:
                uid = await self.database.select_group_uid_by_slug(group_slug)
                if caching:
                    self.cache.set_group(uid, group_slug)
            except RuntimeError:
                pass
        return uid

    async def get_group_slug(self, group_uid: int, caching=True) -> str:
        slug = self.cache.get_group_slug(group_uid)
        if slug is None:
            try:
                slug = await self.database.select_group_slug_by_uid(group_uid)
                if caching:
                    self.cache.set_group(group_uid, slug)
            except RuntimeError:
                pass
        return slug

    async def get_project_uid(
        self, group_uid: int, project_slug: str, caching=True
    ) -> int:
        if not project_slug:
            raise ValueError("The `project_slug` argument is empty.")

        uid = self.cache.get_project_uid(group_uid, project_slug)
        if uid is None:
            try:
                uid = await self.database.select_project_uid_by_group_uid_and_slug(
                    group_uid, project_slug
                )
                if caching:
                    self.cache.set_project(uid, group_uid, project_slug)
            except RuntimeError:
                pass
        return uid

    async def get_permission_uid(self, permission_name: str, caching=True) -> int:
        if not permission_name:
            raise ValueError("The `permission_name` argument is empty.")

        uid = self.cache.get_permission_uid(permission_name)
        if uid is None:
            try:
                uid = await self.database.select_permission_uid_by_name(permission_name)
                if caching:
                    self.cache.set_permission(uid, permission_name)
            except RuntimeError:
                pass
        return uid

    async def get_permission_name(self, permission_uid: int, caching=True) -> str:
        slug = self.cache.get_permission_name(permission_uid)
        if slug is None:
            try:
                slug = await self.database.select_permission_name_by_uid(permission_uid)
                if caching:
                    self.cache.set_permission(permission_uid, slug)
            except RuntimeError:
                pass
        return slug
