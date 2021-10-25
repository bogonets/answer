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
        slug: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        requirements_sha256: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        enable=False,
    ) -> int:
        if plugin not in self.get_daemon_plugins():
            raise ValueError(f"Not exists plugin: {plugin}")

        uid = await self.database.insert_daemon(
            plugin=plugin,
            slug=slug,
            name=name,
            address=address,
            requirements_sha256=requirements_sha256,
            description=description,
            extra=extra,
            enable=enable,
        )

        if requirements_sha256:
            prev_requirements_sha256 = requirements_sha256
        else:
            prev_requirements_sha256 = str()

        updated_hash = await self.daemons.update_daemon(
            plugin,
            slug,
            address,
            prev_requirements_sha256,
            enable,
            self.storage.daemon,
            self.loop,
        )

        if prev_requirements_sha256 != updated_hash:
            await self.database.update_daemon_requirements_sha256_by_uid(
                uid, updated_hash
            )

        return uid

    async def update_daemon(
        self,
        uid: int,
        plugin: Optional[str] = None,
        slug: Optional[str] = None,
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
            slug=slug,
            name=name,
            address=address,
            requirements_sha256=requirements_sha256,
            description=description,
            extra=extra,
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

    def is_running(self, slug: str) -> bool:
        return self.daemons.is_running(slug)

    def status(self, slug: str) -> str:
        return self.daemons.status(slug)

    async def start_daemon(self, slug: str) -> None:
        await self.daemons.start(slug)

    async def stop_daemon(self, slug: str) -> None:
        await self.daemons.stop(slug)
