# -*- coding: utf-8 -*-

from typing import List, Optional

from recc.core.mixin.context_base import ContextBase
from recc.package.package_utils import filter_module_names
from recc.packet.daemon import Daemon, DaemonState


class ContextDaemon(ContextBase):
    def find_daemon_package_names(self) -> List[str]:
        return filter_module_names(self.config.daemon_plugin_prefix)

    async def create_daemon(
        self,
        plugin: str,
        slug: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        enable=False,
    ) -> int:
        if plugin not in self.find_daemon_package_names():
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
        return self._daemons.get_state(slug)

    async def start_daemon(self, slug: str) -> None:
        daemon = await self.get_daemon_by_slug(slug)
        if slug not in self._daemons:
            self._daemons.create(slug, daemon.plugin)

        assert slug in self._daemons
        await self._daemons.start(slug, daemon.address)

    def kill_daemon(self, slug: str) -> None:
        self._daemons.kill(slug)
