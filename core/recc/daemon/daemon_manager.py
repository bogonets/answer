# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, Optional
from asyncio import AbstractEventLoop
from recc.log.logging import recc_daemon_logger as logger
from recc.database.interfaces.db_interface import DbInterface
from recc.daemon.daemon_runner import DaemonRunner


class DaemonManager(Dict[str, DaemonRunner]):
    def add_new_runner(
        self,
        slug: str,
        address: str,
        directory: Path,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        runner = DaemonRunner(Path(directory), address, loop)
        self.__setitem__(slug, runner)

    def is_running(self, slug: str) -> bool:
        return self.__getitem__(slug).is_running()

    def status(self, slug: str) -> str:
        try:
            return self.__getitem__(slug).status
        except KeyError:
            return "unregistered"
        except:  # noqa
            return "error"

    def exists_requirements(self, slug: str) -> bool:
        return self.__getitem__(slug).requirements_path.is_file()

    async def install(
        self, slug: str, prev_requirements_sha256: Optional[str] = None
    ) -> str:
        item = self.__getitem__(slug)
        return await item.install_requirements(prev_requirements_sha256)

    async def start(self, slug: str) -> None:
        await self.__getitem__(slug).open()

    async def stop(self, slug: str) -> None:
        await self.__getitem__(slug).close()

    async def update_daemon(
        self,
        plugin: str,
        slug: str,
        address: str,
        prev_requirements_sha256: str,
        enable: bool,
        plugin_root_directory: Path,
        loop: Optional[AbstractEventLoop] = None,
    ) -> str:
        if not plugin:
            raise RuntimeError("The `plugin` of the daemon must exist.")
        if not slug:
            raise RuntimeError("The `slug` of the daemon must exist.")
        if not address:
            raise RuntimeError("The `address` of the daemon must exist.")

        daemon_directory = plugin_root_directory / plugin
        self.add_new_runner(slug, address, daemon_directory, loop)

        if self.exists_requirements(slug):
            updated_hash = await self.install(slug, prev_requirements_sha256)
        else:
            updated_hash = str()

        if enable:
            await self.start(slug)
            logger.info(f"Started daemon: {slug} -> {address}")

        return updated_hash

    async def open(
        self,
        plugin_root_directory: Path,
        database: DbInterface,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        daemons = await database.select_daemons()
        for daemon in daemons:
            if daemon.uid is None:
                raise RuntimeError("The `uid` of the daemon must exist.")
            if not daemon.plugin:
                raise RuntimeError("The `plugin` of the daemon must exist.")
            if not daemon.slug:
                raise RuntimeError("The `slug` of the daemon must exist.")
            if not daemon.address:
                raise RuntimeError("The `address` of the daemon must exist.")

            if daemon.requirements_sha256:
                prev_requirements_sha256 = daemon.requirements_sha256
            else:
                prev_requirements_sha256 = str()
            enable = True if daemon.enable else False

            updated_hash = await self.update_daemon(
                daemon.plugin,
                daemon.slug,
                daemon.address,
                prev_requirements_sha256,
                enable,
                plugin_root_directory,
                loop,
            )

            if prev_requirements_sha256 != updated_hash:
                await database.update_daemon_requirements_sha256_by_uid(
                    daemon.uid, updated_hash
                )

    async def close(self) -> None:
        for key, runner in self.items():
            if runner.is_opened():
                await runner.close()
                logger.info(f"Closed daemon: {key}")
