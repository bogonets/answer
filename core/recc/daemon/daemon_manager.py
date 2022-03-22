# -*- coding: utf-8 -*-

import os
from typing import Dict, Optional
from asyncio import AbstractEventLoop
from overrides import overrides
from recc.daemon.daemon_runner import DaemonRunnerCallbacks, DaemonRunner
from recc.daemon.daemon_state import DaemonState
from recc.filesystem.permission import (
    test_readable_directory,
    test_writable_directory,
    test_readable_file,
    prepare_writable_directory,
)


class _RunnerCallback(DaemonRunnerCallbacks):
    def __init__(self, work_dir: str, slug: str, logging=True):
        self._work_dir = work_dir
        self._slug = slug
        self._logging = logging

    @overrides
    async def on_created_venv(self, root: str) -> None:
        pass

    @overrides
    async def on_stdout(self, data: bytes) -> None:
        pass

    @overrides
    async def on_stderr(self, data: bytes) -> None:
        pass

    @overrides
    async def on_daemon_done(self, exit_code: int) -> None:
        pass

    @overrides
    async def on_pip_install_stdout(self, data: bytes) -> None:
        pass

    @overrides
    async def on_pip_install_stderr(self, data: bytes) -> None:
        pass

    @overrides
    async def on_pip_install_done(self, exit_code: int) -> None:
        pass


class DaemonManager:
    def __init__(
        self,
        daemon_work_root_dir: str,
        daemon_venv_root_dir: str,
        pip_download_dir: str,
        pip_timeout: Optional[float] = None,
        logging=True,
        *,
        isolate_ensure_pip=True,
    ):
        test_writable_directory(daemon_work_root_dir)
        test_writable_directory(daemon_venv_root_dir)

        self._daemon_work_root_dir = daemon_work_root_dir
        self._daemon_venv_root_dir = daemon_venv_root_dir
        self._pip_download_dir = pip_download_dir
        self._pip_timeout = pip_timeout
        self._logging = logging
        self._isolate_ensure_pip = isolate_ensure_pip
        self._daemons: Dict[str, DaemonRunner] = dict()

    def get_state(self, slug: str) -> DaemonState:
        try:
            return self._daemons[slug].state
        except KeyError:
            return DaemonState.Unregistered
        except:  # noqa
            return DaemonState.Unknown

    def create_runner(
        self,
        slug: str,
        plugin_dir: str,
        plugin_script_path: str,
    ) -> None:
        if not slug:
            raise ValueError("The `slug` of the daemon must exist.")

        test_readable_directory(plugin_dir)
        test_readable_file(plugin_script_path)

        work_dir = os.path.join(self._daemon_work_root_dir, slug)
        venv_dir = os.path.join(self._daemon_venv_root_dir, slug)

        prepare_writable_directory(work_dir)
        prepare_writable_directory(venv_dir)

        self._daemons[slug] = DaemonRunner(
            plugin_dir=plugin_dir,
            plugin_script_path=plugin_script_path,
            work_dir=work_dir,
            venv_dir=venv_dir,
            system_site_packages=False,
            pip_timeout=self._pip_timeout,
            pip_download_dir=self._pip_download_dir,
            callbacks=_RunnerCallback(work_dir, slug, self._logging),
            isolate_ensure_pip=self._isolate_ensure_pip,
        )

    async def start_daemon(
        self,
        slug: str,
        address: str,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        await self._daemons[slug].start_daemon(address, loop)

    def interrupt_daemon(self, slug: str) -> None:
        self._daemons[slug].interrupt_daemon()

    def kill_daemon(self, slug: str) -> None:
        self._daemons[slug].kill_daemon()

    # async def update_daemon(
    #     self,
    #     plugin: str,
    #     slug: str,
    #     address: str,
    #     prev_requirements_sha256: str,
    #     enable: bool,
    #     plugin_root_directory: Path,
    #     loop: Optional[AbstractEventLoop] = None,
    # ) -> str:
    #     if not plugin:
    #         raise RuntimeError("The `plugin` of the daemon must exist.")
    #     if not slug:
    #         raise RuntimeError("The `slug` of the daemon must exist.")
    #     if not address:
    #         raise RuntimeError("The `address` of the daemon must exist.")
    #
    #     daemon_directory = plugin_root_directory / plugin
    #     self.add_new_runner(slug, address, daemon_directory, loop)
    #
    #     # if self.exists_requirements(slug):
    #     #     updated_hash = await self.install(slug, prev_requirements_sha256)
    #     # else:
    #     #     updated_hash = str()
    #     #
    #     # if enable:
    #     #     await self.start(slug)
    #     #     logger.info(f"Started daemon: {slug} -> {address}")
    #     #
    #     # return updated_hash

    # async def open(
    #     self,
    #     plugin_root_directory: str,
    #     database: DbInterface,
    #     loop: Optional[AbstractEventLoop] = None,
    # ) -> None:
    #     daemons = await database.select_daemons()
    #     for daemon in daemons:
    #         if daemon.uid is None:
    #             raise RuntimeError("The `uid` of the daemon must exist.")
    #         if not daemon.plugin:
    #             raise RuntimeError("The `plugin` of the daemon must exist.")
    #         if not daemon.slug:
    #             raise RuntimeError("The `slug` of the daemon must exist.")
    #         if not daemon.address:
    #             raise RuntimeError("The `address` of the daemon must exist.")
    #
    #         # if daemon.requirements_sha256:
    #         #     prev_requirements_sha256 = daemon.requirements_sha256
    #         # else:
    #         #     prev_requirements_sha256 = str()
    #         # enable = True if daemon.enable else False
    #         #
    #         # updated_hash = await self.update_daemon(
    #         #     daemon.plugin,
    #         #     daemon.slug,
    #         #     daemon.address,
    #         #     prev_requirements_sha256,
    #         #     enable,
    #         #     Path(plugin_root_directory),
    #         #     loop,
    #         # )
    #         #
    #         # if prev_requirements_sha256 != updated_hash:
    #         #     await database.update_daemon_requirements_sha256_by_uid(
    #         #         daemon.uid, updated_hash
    #         #     )

    # async def close(self) -> None:
    #     for key, runner in self._daemons.items():
    #         if runner.is_opened():
    #             await runner.close()
    #             logger.info(f"Closed daemon: {key}")

    # async def register(
    #     self,
    #     connection_timeout: Optional[float] = None,
    #     query_timeout: Optional[float] = None,
    # ) -> None:
    #     wait_timeout = connection_timeout if connection_timeout else 120.0
    #     client_timeout = query_timeout if query_timeout else 120.0
    #
    #     runner_count = len(self._daemons)
    #     for index, runner in enumerate(self._daemons.values()):
    #         address = runner.address_for_client
    #         client: Optional[DaemonClient] = DaemonClient(address, client_timeout)
    #
    #         logger.debug(
    #             f"[{index}/{runner_count}] "
    #             f"Connecting to daemon server ... {address} "
    #             f"(Wait timeout: {wait_timeout}s)"
    #         )
    #
    #         try:
    #             assert client is not None
    #             await wait_for(client.open(), timeout=wait_timeout)
    #         except AsyncioTimeoutError:
    #             logger.error("Daemon server connection timed out.")
    #             client = None
    #         except BaseException as e:  # noqa
    #             logger.error(
    #                 f"Failed to connect to daemon server for unknown reason. {e}"
    #             )
    #             client = None
    #         else:
    #             logger.info("You have successfully connected to the daemon server.")
    #
    #         if not client:
    #             continue
    #
    #         try:
    #             await client.register()
    #             logger.info("The daemon's register API call was successful.")
    #         except BaseException as e:  # noqa
    #             logger.error(f"The daemon's Init API call failed. {e}")
    #         finally:
    #             await client.close()
