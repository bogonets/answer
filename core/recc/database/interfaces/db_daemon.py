# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional

from recc.database.struct.daemon import Daemon


class DbDaemon(metaclass=ABCMeta):
    """
    Database daemon interface.
    """

    @abstractmethod
    async def insert_daemon(
        self,
        plugin: str,
        slug: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        enable=False,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_daemon_by_uid(
        self,
        uid: int,
        plugin: Optional[str] = None,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        enable: Optional[bool] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_daemon_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_daemon_by_slug(self, slug: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_daemon_by_uid(self, uid: int) -> Daemon:
        raise NotImplementedError

    @abstractmethod
    async def select_daemon_by_slug(self, slug: str) -> Daemon:
        raise NotImplementedError

    @abstractmethod
    async def select_daemon_uid_by_slug(self, slug: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_daemon_address_by_slug(self, slug: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def select_daemons(self) -> List[Daemon]:
        raise NotImplementedError
