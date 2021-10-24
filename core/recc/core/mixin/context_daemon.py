# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.daemon import Daemon
from recc.daemon.daemon_runner import DAEMON_SCRIPT_EXTENSION


class ContextDaemon(ContextBase):
    def get_daemon_plugins(self) -> List[str]:
        result = list()
        for directory in self.storage.find_daemon_dirs():
            script_path = directory / (directory.name + DAEMON_SCRIPT_EXTENSION)
            if script_path.is_file():
                result.append(directory.name)
        return result

    async def create_daemon(
        self,
        plugin: str,
        name: str,
        address: Optional[str] = None,
        requirements_sha256: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        enable=False,
    ) -> int:
        if plugin not in self.get_daemon_plugins():
            raise ValueError(f"Not exists plugin: {plugin}")
        return await self.database.insert_daemon(
            plugin=plugin,
            name=name,
            address=address,
            requirements_sha256=requirements_sha256,
            description=description,
            extra=extra,
            enable=enable,
        )

    async def update_daemon(
        self,
        uid: int,
        plugin: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        requirements_sha256: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        enable: Optional[bool] = None,
    ) -> None:
        await self.database.update_daemon_by_uid(
            uid=uid,
            plugin=plugin,
            name=name,
            address=address,
            requirements_sha256=requirements_sha256,
            description=description,
            extra=extra,
            enable=enable,
        )

    async def delete_daemon(self, uid: int) -> None:
        await self.database.delete_daemon_by_uid(uid)

    async def delete_daemon_by_name(self, name: str) -> None:
        await self.database.delete_daemon_by_name(name)

    async def get_daemon(self, uid: int) -> Daemon:
        return await self.database.select_daemon_by_uid(uid)

    async def get_daemon_uid_by_name(self, name: str) -> int:
        return await self.database.select_daemon_uid_by_name(name)

    async def get_daemon_address_by_name(self, name: str) -> str:
        return await self.database.select_daemon_address_by_name(name)

    async def get_daemon_by_name(self, name: str) -> Daemon:
        return await self.database.select_daemon_by_name(name)

    async def get_daemons(self) -> List[Daemon]:
        return await self.database.select_daemons()

    def is_running(self, name: str) -> bool:
        return self.daemons.is_running(name)

    async def start_daemon(self, name: str) -> None:
        address = await self.database.select_daemon_address_by_name(name)
        await self.daemons.start(name, address)

    async def stop_daemon(self, name: str) -> None:
        await self.daemons.stop(name)
