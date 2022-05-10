# -*- coding: utf-8 -*-

import os
from typing import Dict, Optional
from asyncio import AbstractEventLoop
from overrides import overrides
from logging import getLogger, INFO, WARNING
from recc.logging.logging import LOGGER_NAME_DAEMON_RPC
from recc.daemon.daemon_runner import DaemonRunnerCallbacks, DaemonRunner
from recc.daemon.daemon_state import DaemonState
from recc.filesystem.permission import (
    test_readable_directory,
    test_writable_directory,
    test_readable_file,
    prepare_writable_directory,
)


class _RunnerCallback(DaemonRunnerCallbacks):
    def __init__(
        self,
        work_dir: str,
        slug: str,
        encoding="utf-8",
        stdout_level=INFO,
        stderr_level=WARNING,
    ):
        self._work_dir = work_dir
        self._slug = slug
        self._logger = getLogger(LOGGER_NAME_DAEMON_RPC + "." + slug)
        self._encoding = encoding
        self._stdout_level = stdout_level
        self._stderr_level = stderr_level

    @overrides
    async def on_created_venv(self, result: bool, root: str) -> None:
        if result:
            self._logger.info(f"Created a virtual environment: '{root}'")
        else:
            self._logger.error(f"Failed to create virtual environment: '{root}'")

    @overrides
    async def on_stdout(self, data: bytes) -> None:
        self._logger.log(self._stdout_level, str(data, encoding=self._encoding))

    @overrides
    async def on_stderr(self, data: bytes) -> None:
        self._logger.log(self._stderr_level, str(data, encoding=self._encoding))

    @overrides
    async def on_daemon_done(self, exit_code: int) -> None:
        if exit_code == 0:
            self._logger.info("The daemon exited normally")
        else:
            self._logger.warning(f"The daemon exited abnormally: {exit_code}")

    @overrides
    async def on_pip_install_stdout(self, data: bytes) -> None:
        self._logger.log(self._stdout_level, str(data, encoding=self._encoding))

    @overrides
    async def on_pip_install_stderr(self, data: bytes) -> None:
        self._logger.log(self._stderr_level, str(data, encoding=self._encoding))

    @overrides
    async def on_pip_install_done(self, exit_code: int) -> None:
        if exit_code == 0:
            self._logger.info("The pip exited normally")
        else:
            self._logger.warning(f"The pip exited abnormally: {exit_code}")


class DaemonManager:
    def __init__(
        self,
        daemon_work_root_dir: str,
        daemon_venv_root_dir: str,
        pip_download_dir: str,
        pip_timeout: Optional[float] = None,
        *,
        isolate_ensure_pip=True,
    ):
        test_writable_directory(daemon_work_root_dir)
        test_writable_directory(daemon_venv_root_dir)

        self._daemon_work_root_dir = daemon_work_root_dir
        self._daemon_venv_root_dir = daemon_venv_root_dir
        self._pip_download_dir = pip_download_dir
        self._pip_timeout = pip_timeout
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
            callbacks=_RunnerCallback(work_dir, slug),
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

    async def close(self):
        pass
