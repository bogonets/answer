# -*- coding: utf-8 -*-

from typing import Optional, List
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.daemon import Daemon
from recc.daemon.daemon_runner import DAEMON_SCRIPT_EXTENSION
from recc.daemon.daemon_state import DaemonState


class ContextDaemon(ContextBase):
    def get_daemon_plugins(self) -> List[str]:
        result = list()
        for directory in self.local_storage.find_daemon_dirs():
            script_path = directory / (directory.name + DAEMON_SCRIPT_EXTENSION)
            if script_path.is_file():
                result.append(directory.name)
        return result

    async def create_daemon(
        self,
        plugin: str,
        slug: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        enable=False,
    ) -> int:
        if plugin not in self.get_daemon_plugins():
            raise ValueError(f"Not exists plugin: {plugin}")

        return await self.database.insert_daemon(
            plugin=plugin,
            slug=slug,
            name=name,
            address=address,
            description=description,
            enable=enable,
        )

    async def update_daemon(
        self,
        uid: int,
        plugin: Optional[str] = None,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        enable: Optional[bool] = None,
    ) -> None:
        await self.database.update_daemon_by_uid(
            uid=uid,
            plugin=plugin,
            slug=slug,
            name=name,
            address=address,
            description=description,
            enable=enable,
        )

    async def delete_daemon(self, uid: int) -> None:
        await self.database.delete_daemon_by_uid(uid)

    async def delete_daemon_by_slug(self, slug: str) -> None:
        await self.database.delete_daemon_by_slug(slug)

    async def get_daemon(self, uid: int) -> Daemon:
        return await self.database.select_daemon_by_uid(uid)

    async def get_daemon_uid_by_slug(self, slug: str) -> int:
        return await self.database.select_daemon_uid_by_slug(slug)

    async def get_daemon_address_by_slug(self, slug: str) -> str:
        return await self.database.select_daemon_address_by_slug(slug)

    async def get_daemon_by_slug(self, slug: str) -> Daemon:
        return await self.database.select_daemon_by_slug(slug)

    async def get_daemons(self) -> List[Daemon]:
        return await self.database.select_daemons()

    def get_daemon_state(self, slug: str) -> DaemonState:
        return self.daemons.get_state(slug)

    async def start_daemon(self, slug: str) -> None:
        address = await self.get_daemon_address_by_slug(slug)
        await self.daemons.start_daemon(slug, address)

    def kill_daemon(self, slug: str) -> None:
        self.daemons.kill_daemon(slug)
