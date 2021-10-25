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
        slug: str,
        directory: Path,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        runner = DaemonRunner(Path(directory), loop)
        self.__setitem__(slug, runner)

    def exists_requirements(self, slug: str) -> bool:
        return self.__getitem__(slug).requirements_path.is_file()

    async def install(
        self, slug: str, requirements_sha256: Optional[str] = None
    ) -> str:
        return await self.__getitem__(slug).install_requirements(requirements_sha256)

    def is_running(self, slug: str) -> bool:
        return self.__getitem__(slug).is_running()

    def status(self, slug: str) -> str:
        try:
            return self.__getitem__(slug).status
        except KeyError:
            return "unregistered"
        except:  # noqa
            return "error"

    async def start(self, slug: str, address: str) -> None:
        await self.__getitem__(slug).open(address)

    async def stop(self, slug: str) -> None:
        await self.__getitem__(slug).close()

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
            if not daemon.plugin:
                raise RuntimeError("The `plugin` of the daemon must exist.")
            if not daemon.slug:
                raise RuntimeError("The `slug` of the daemon must exist.")

            daemon_directory = plugin_root_directory / daemon.plugin
            self.create_runner(daemon.slug, daemon_directory, loop)

            if self.exists_requirements(daemon.slug):
                updated_hash = await self.install(
                    daemon.slug, daemon.requirements_sha256
                )
                if daemon.requirements_sha256 != updated_hash:
                    await database.update_daemon_requirements_sha256_by_uid(
                        daemon.uid, updated_hash
                    )

            if daemon.enable:
                if not daemon.address:
                    raise RuntimeError("The `address` of the daemon must exist.")

                await self.start(daemon.slug, daemon.address)
                logger.info(f"Started daemon: {daemon.slug} -> {daemon.address}")

    async def close(self) -> None:
        for key, runner in self.items():
            if runner.is_opened():
                await runner.close()
                logger.info(f"Closed daemon: {key}")
