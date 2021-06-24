# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop
from recc.argparse.config.core_config import CoreConfig
from recc.session.session import SessionPairFactory
from recc.storage.async_sm import AsyncStorageManager
from recc.container.container_manager_interface import ContainerManagerInterface
from recc.cache.async_cs_interface import AsyncCacheStoreInterface
from recc.database.async_db_interface import AsyncDatabaseInterface
from recc.rpc.async_rpc_client_manager import AsyncRpcClientManager


class ContextBase:

    _loop: AbstractEventLoop
    _config: CoreConfig
    _signature: str
    _sm: AsyncStorageManager
    _sf: SessionPairFactory
    _cm: ContainerManagerInterface
    _container_key: str
    _cs: AsyncCacheStoreInterface
    _db: AsyncDatabaseInterface
    _tm: AsyncRpcClientManager

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
    def sm(self):
        """
        Storage Manager property.
        """
        return self._sm

    @property
    def sf(self):
        """
        Session Factory property.
        """
        assert self._sf is not None
        return self._sf

    @property
    def cm(self):
        """
        Container Manager property.
        """
        assert self._cm is not None
        if not self._cm.is_open():
            raise ValueError("The container-manager is not open")
        return self._cm

    def is_cm_open(self) -> bool:
        assert self._cm is not None
        return self._cm.is_open()

    def is_host_mode(self) -> bool:
        return len(self._container_key) == 0

    def is_guest_mode(self) -> bool:
        return not self.is_host_mode()

    @property
    def container_key(self) -> str:
        return self._container_key

    @property
    def cs(self):
        """
        Cache Store property.
        """
        assert self._cs is not None
        if not self._cs.is_open():
            raise ValueError("The cache-store is not open")
        return self._cs

    def is_cs_open(self) -> bool:
        assert self._cs is not None
        return self._cs.is_open()

    @property
    def db(self):
        """
        Database property.
        """
        assert self._db is not None
        if not self._db.is_open():
            raise ValueError("The database is not open")
        return self._db

    def is_db_open(self) -> bool:
        assert self._db is not None
        return self._db.is_open()

    async def get_database_version(self) -> str:
        return await self.db.get_database_version()

    @property
    def tm(self):
        """
        Task Manager
        """
        assert self._tm is not None
        return self._tm
