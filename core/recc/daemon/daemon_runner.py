# -*- coding: utf-8 -*-

from typing import Optional
from pathlib import Path
from hashlib import sha256
from asyncio import AbstractEventLoop, get_event_loop, run_coroutine_threadsafe

from recc.logging.logging import recc_daemon_logger as logger
from recc.network.uds import is_uds_family
from recc.subprocess.async_subprocess import AsyncSubprocess
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc.argparse.config.global_config import ARG_LOG_SIMPLY
from recc.argparse.config.daemon_config import (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_FILE,
    ARG_DAEMON_PACKAGES_DIR,
)

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

        self.requirements_path = directory / DAEMON_REQUIREMENTS_TXT
        self.venv_dir = directory / DAEMON_VENV_DIRECTORY
        self.venv = AsyncVirtualEnvironment(str(self.venv_dir))

        if self.requirements_path.is_file():
            requirements_content = self.requirements_path.read_bytes()
            self.requirements_sha256 = sha256(requirements_content).hexdigest()
        else:
            self.requirements_sha256 = ""
            logger.warning(f"Daemon {DAEMON_REQUIREMENTS_TXT} not found")

        self.process: Optional[AsyncSubprocess] = None
        self.process_join_timeout = DEFAULT_PROCESS_JOIN_TIMEOUT
        self.output_encoding = "utf-8"

    @property
    def address_for_client(self) -> str:
        if is_uds_family(self.address):
            return self.address

        # TODO: gRPC address pattern parsing ...

        address_and_port = self.address.split(":")[0]
        if address_and_port[0] == "0.0.0.0":
            if len(address_and_port) == 2:
                return f"localhost:{address_and_port[1]}"
            else:
                return "localhost"
        else:
            return self.address

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

    async def install_requirements(
        self, prev_requirements_sha256: Optional[str] = None
    ) -> str:
        if self.requirements_sha256 and prev_requirements_sha256 is not None:
            if prev_requirements_sha256 == self.requirements_sha256:
                logger.debug("The requirements file has not changed")
                return self.requirements_sha256

        await self.venv.create_if_not_exists()

        py_for_pip = self.venv.create_python_subprocess()
        logger.info(f"[Daemon:{self.name}] Initiate package installation by PIP.")
        proc = await py_for_pip.start_pip(
            "install",
            "-r",
            self.requirements_path,
            stdout_callback=self._stdout_callback,
            stderr_callback=self._stderr_callback,
            writable=False,
        )

        pip_exit_code = await proc.wait()
        if pip_exit_code != 0:
            raise RuntimeError(f"PIP Installation failed: {pip_exit_code}")

        logger.info(f"[Daemon:{self.name}] Completed package installation by PIP.")
        return self.requirements_sha256

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
            raise RuntimeError("Already process.")

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
            raise RuntimeError("Not exists process.")

        # self.process.send_signal(SIGINT)
        self.process.kill()
        await self.process.wait()
        self.process = None
