# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, Optional
from asyncio import AbstractEventLoop
from recc.log.logging import recc_daemon_logger as logger
from recc.database.interfaces.db_interface import DbInterface
from recc.daemon.daemon_runner import DaemonRunner


class DaemonManager(Dict[str, DaemonRunner]):
    def create_runner(
        self,
        name: str,
        directory: Path,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        runner = DaemonRunner(Path(directory), loop)
        self.__setitem__(name, runner)

    async def install(
        self,
        name: str,
        requirements_sha256: Optional[str] = None,
    ) -> str:
        return await self.__getitem__(name).install_requirements(requirements_sha256)

    def is_running(self, name: str) -> bool:
        return self.__getitem__(name).is_running()

    async def start(self, name: str, address: str) -> None:
        await self.__getitem__(name).open(address)

    async def stop(self, name: str) -> None:
        await self.__getitem__(name).close()

    async def open(
        self,
        plugin_root_directory: Path,
        database: DbInterface,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        daemons = await database.select_daemons()
        for daemon in daemons:
            if not daemon.uid:
                raise RuntimeError("The `uid` of the daemon must exist.")
            if not daemon.name:
                raise RuntimeError("The `name` of the daemon must exist.")
            if not daemon.plugin:
                raise RuntimeError("The `plugin` of the daemon must exist.")

            daemon_directory = plugin_root_directory / daemon.plugin
            self.create_runner(daemon.name, daemon_directory, loop)

            updated_hash = await self.install(daemon.name, daemon.requirements_sha256)
            if daemon.requirements_sha256 != updated_hash:
                await database.update_daemon_requirements_sha256_by_uid(
                    daemon.uid, updated_hash
                )

            if daemon.enable:
                if not daemon.address:
                    raise RuntimeError("The `address` of the daemon must exist.")

                await self.start(daemon.name, daemon.address)
                logger.info(f"Started daemon: {daemon.name} -> {daemon.address}")

    async def close(self) -> None:
        for key, runner in self.items():
            if runner.is_opened():
                await runner.close()
                logger.info(f"Closed daemon: {key}")
