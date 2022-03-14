# -*- coding: utf-8 -*-

import os
from typing import Optional
from pathlib import Path
from asyncio import (
    AbstractEventLoop,
    get_event_loop,
    run_coroutine_threadsafe,
    Task,
    wait_for,
    shield,
    get_running_loop,
)
from recc.logging.logging import recc_daemon_logger as logger
from recc.subprocess.async_subprocess import AsyncSubprocess
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc.argparse.config.global_config import ARG_LOG_SIMPLY
from recc.argparse.command import Command
from recc.argparse.config.daemon_config import (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_FILE,
    ARG_DAEMON_PACKAGES_DIR,
)
from recc.filesystem.permission import (
    is_readable_file,
    is_readable_dir,
    is_writable_dir,
)
from recc.daemon.daemon_state import DaemonState


DAEMON_SCRIPT_EXTENSION = ".py"
DAEMON_REQUIREMENTS_TXT = "requirements.txt"
DAEMON_VENV_DIRECTORY = ".venv"

DEFAULT_PROCESS_JOIN_TIMEOUT = 30.0


class DaemonRunner:
    def __init__(
        self,
        directory: Path,
        address: str,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        assert directory.is_dir()

        self.directory = directory
        self.address = address
        self.loop = loop if loop else get_event_loop()

        self.name = directory.name
        self.script_path = directory / (self.name + DAEMON_SCRIPT_EXTENSION)

        if not self.script_path.is_file():
            raise FileNotFoundError(f"Daemon script not found: {self.script_path}")

        self.venv_dir = directory / DAEMON_VENV_DIRECTORY
        self.venv = AsyncVirtualEnvironment(str(self.venv_dir))

        self.process: Optional[AsyncSubprocess] = None
        self.process_join_timeout = DEFAULT_PROCESS_JOIN_TIMEOUT
        self.output_encoding = "utf-8"

    # @property
    # def address_for_client(self) -> str:
    #     if is_uds_family(self.address):
    #         return self.address
    #
    #     # TODO: gRPC address pattern parsing ...
    #
    #     address_and_port = self.address.split(":")[0]
    #     if address_and_port[0] == "0.0.0.0":
    #         if len(address_and_port) == 2:
    #             return f"localhost:{address_and_port[1]}"
    #         else:
    #             return "localhost"
    #     else:
    #         return self.address

    @staticmethod
    def is_daemon_plugin_directory(directory: Path) -> bool:
        if not directory.is_dir():
            return False
        script_path = directory / (directory.name + DAEMON_SCRIPT_EXTENSION)
        return script_path.is_file()

    async def _flush_stdout_callback(self, text: str) -> None:
        logger.info(f"[Daemon:{self.name}:stdout] {text}")

    async def _flush_stderr_callback(self, text: str) -> None:
        logger.error(f"[Daemon:{self.name}:stderr] {text}")

    def _stdout_callback(self, data: bytes) -> None:
        message = str(data, encoding=self.output_encoding).strip()
        if message:
            run_coroutine_threadsafe(self._flush_stdout_callback(message), self.loop)

    def _stderr_callback(self, data: bytes) -> None:
        message = str(data, encoding=self.output_encoding).strip()
        if message:
            run_coroutine_threadsafe(self._flush_stderr_callback(message), self.loop)

    # async def install_requirements(
    #     self, prev_requirements_sha256: Optional[str] = None
    # ) -> str:
    #     if self.requirements_sha256 and prev_requirements_sha256 is not None:
    #         if prev_requirements_sha256 == self.requirements_sha256:
    #             logger.debug("The requirements file has not changed")
    #             return self.requirements_sha256
    #
    #     await self.venv.create_if_not_exists()
    #
    #     py_for_pip = self.venv.create_python_subprocess()
    #     logger.info(f"[Daemon:{self.name}] Initiate package installation by PIP.")
    #     proc = await py_for_pip.start_pip(
    #         "install",
    #         "-r",
    #         self.requirements_path,
    #         stdout_callback=self._stdout_callback,
    #         stderr_callback=self._stderr_callback,
    #         writable=False,
    #     )
    #
    #     pip_exit_code = await proc.wait()
    #     if pip_exit_code != 0:
    #         raise RuntimeError(f"PIP Installation failed: {pip_exit_code}")
    #
    #     logger.info(f"[Daemon:{self.name}] Completed package installation by PIP.")
    #     return self.requirements_sha256

    def is_opened(self) -> bool:
        return self.process is not None

    def is_running(self) -> bool:
        if not self.process:
            return False
        return self.process.is_running()

    @property
    def status(self) -> str:
        if not self.process:
            return "unallocated"
        return self.process.status

    async def open(self) -> None:
        if self.process is not None:
            raise RuntimeError(f"Already process (pid={self.process.get_pid()})")

        # [WARNING] Do not use the `self.venv.create_python_subprocess()`
        python_for_daemon = AsyncPythonSubprocess.create_system()

        subcommands = [
            "-m",
            "recc",
            ARG_LOG_SIMPLY.long_key,
            "daemon",
            ARG_DAEMON_ADDRESS.long_key,
            self.address,
            ARG_DAEMON_FILE.long_key,
            self.script_path,
            ARG_DAEMON_PACKAGES_DIR.long_key,
            self.venv.site_packages_dir,
        ]
        self.process = await python_for_daemon.start_python(
            *subcommands,
            stdout_callback=self._stdout_callback,
            stderr_callback=self._stderr_callback,
            writable=False,
        )
        logger.info(f"[Daemon:{self.name}] Start process: {subcommands}")

    async def close(self) -> None:
        if self.process is None:
            raise RuntimeError("Not exists process")

        # self.process.send_signal(SIGINT)
        self.process.kill()
        await self.process.wait()
        self.process = None


class DaemonRunner2:
    def __init__(
        self,
        plugin_dir: str,
        plugin_script_path: str,
        work_dir: str,
        venv_dir: str,
        system_site_packages=False,
        pip_timeout: Optional[float] = None,
    ) -> None:
        assert os.path.isdir(plugin_dir)
        assert is_readable_dir(plugin_dir)

        assert os.path.isfile(plugin_script_path)
        assert is_readable_file(plugin_script_path)

        assert os.path.isdir(work_dir)
        assert is_writable_dir(work_dir)

        assert os.path.isdir(venv_dir)
        assert is_readable_dir(venv_dir)

        self._plugin_dir = plugin_dir
        self._plugin_script_path = plugin_script_path
        self._work_dir = work_dir
        self._venv = AsyncVirtualEnvironment(
            root_directory=venv_dir,
            system_site_packages=system_site_packages,
            pip_timeout=pip_timeout,
        )

        self._creator_task: Optional[Task] = None
        self._daemon_process: Optional[AsyncSubprocess] = None
        self._pip_process: Optional[AsyncSubprocess] = None

    @staticmethod
    async def _timeout_wrapper(coro, timeout: Optional[float] = None) -> None:
        if timeout is not None:
            assert timeout > 0
            await wait_for(coro, timeout=timeout)
        else:
            await coro

    async def cancel_creator_task(self) -> None:
        if self._creator_task is None:
            return

        if self._creator_task.done():
            return

        self._creator_task.cancel()
        try:
            await self._creator_task
        except:  # noqa
            pass

    async def join_creator_task(self, timeout: Optional[float] = None) -> None:
        if self._creator_task is None:
            raise RuntimeError("The task being created does not exist")

        if timeout is not None:
            assert timeout > 0
            await wait_for(shield(self._creator_task), timeout=timeout)
        else:
            await self._creator_task

    async def create_venv(
        self,
        timeout: Optional[float] = None,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        if self._creator_task is not None:
            raise RuntimeError("It is already being created")

        event_loop = loop if loop else get_running_loop()
        self._creator_task = event_loop.create_task(
            self._timeout_wrapper(self._venv.create_if_not_exists(), timeout)
        )

    @property
    def plugin_dir(self):
        return self._plugin_dir

    @property
    def plugin_script_path(self):
        return self._plugin_script_path

    @property
    def work_dir(self):
        return self._work_dir

    @property
    def venv_dir(self):
        return self._venv.root

    @property
    def exists(self) -> bool:
        return self._venv.exists

    @property
    def python_executable(self) -> str:
        return self._venv.env_exe

    @property
    def pip_executable(self) -> str:
        return self._venv.pip_exe

    @property
    def state(self) -> DaemonState:
        # Make sure the environment is being created.
        if self._creator_task is not None:
            if not self._creator_task.done():
                return DaemonState.EnvCreating

        if not self.exists:
            return DaemonState.EnvNotFound

        if self._daemon_process is None:
            return DaemonState.Down

        return DaemonState.from_process_status(self._daemon_process.status)

    def _stdout_callback(self, data: bytes) -> None:
        pass

    def _stderr_callback(self, data: bytes) -> None:
        pass

    async def open(self, address: str) -> None:
        if self._daemon_process is not None:
            pid = self._daemon_process.get_pid()
            raise RuntimeError(f"Already process (pid={pid})")

        # [WARNING] Do not use the `self.venv.create_python_subprocess()`
        python_for_daemon = self._venv.create_python_subprocess()

        subcommands = [
            "-m",
            "recc",
            ARG_LOG_SIMPLY.long_key,
            Command.daemon.name,
            ARG_DAEMON_ADDRESS.long_key,
            address,
            ARG_DAEMON_FILE.long_key,
            self._plugin_script_path,
            ARG_DAEMON_PACKAGES_DIR.long_key,
            self._venv.site_packages_dir,
        ]

        self._daemon_process = await python_for_daemon.start_python(
            *subcommands,
            stdout_callback=self._stdout_callback,
            stderr_callback=self._stderr_callback,
            cwd=self._work_dir,
            writable=False,
        )

    async def close(self) -> None:
        if self._daemon_process is None:
            raise RuntimeError("Not exists process")

        # self.process.send_signal(SIGINT)
        self._daemon_process.kill()
        await self._daemon_process.wait()
        self._daemon_process = None
