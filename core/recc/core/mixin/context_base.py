# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop
from recc.argparse.config.core_config import CoreConfig
from recc.session.session import SessionPairFactory
from recc.storage.core_storage import CoreStorage
from recc.container.container_manager_interface import ContainerManagerInterface
from recc.cache.async_cs_interface import AsyncCacheStoreInterface
from recc.database.async_db_interface import AsyncDatabaseInterface
from recc.task.task_connection_pool import TaskConnectionPool
from recc.resource.port_manager import PortManager


class ContextBase:

    _loop: AbstractEventLoop
    _config: CoreConfig
    _signature: str
    _storage: CoreStorage
    _session_factory: SessionPairFactory
    _container: ContainerManagerInterface
    _container_key: str
    _cache: AsyncCacheStoreInterface
    _database: AsyncDatabaseInterface
    _tasks: TaskConnectionPool
    _ports: PortManager

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
        return await self.database.get_database_version()

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
