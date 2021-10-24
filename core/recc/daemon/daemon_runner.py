# -*- coding: utf-8 -*-

from typing import Optional
from io import BytesIO, SEEK_SET
from signal import SIGINT
from pathlib import Path
from hashlib import sha256
from asyncio import AbstractEventLoop, get_event_loop, run_coroutine_threadsafe

from recc.log.logging import recc_daemon_logger as logger
from recc.subprocess.async_subprocess import AsyncSubprocess
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc.daemon.daemon_client import DaemonClient, create_daemon_client

DAEMON_SCRIPT_EXTENSION = ".py"
DAEMON_REQUIREMENTS_TXT = "requirements.txt"
DAEMON_VENV_DIRECTORY = ".venv"

DEFAULT_PROCESS_JOIN_TIMEOUT = 30.0
DEFAULT_BUFFER_FLUSH_SIZE = 256


def _flush_buffer(buffer: BytesIO, encoding: str) -> str:
    result = str(buffer.getvalue(), encoding=encoding)
    buffer.truncate(0)
    buffer.seek(0, SEEK_SET)
    return result


class DaemonRunner:
    @staticmethod
    def is_daemon_plugin_directory(directory: Path) -> bool:
        if not directory.is_dir():
            return False
        script_path = directory / (directory.name + DAEMON_SCRIPT_EXTENSION)
        return script_path.is_file()

    def __init__(
        self,
        directory: Path,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        assert directory.is_dir()

        self.directory = directory
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

        self.client: Optional[DaemonClient] = None
        self.process: Optional[AsyncSubprocess] = None
        self.process_join_timeout = DEFAULT_PROCESS_JOIN_TIMEOUT
        self.buffer_stdout = BytesIO()
        self.buffer_stderr = BytesIO()
        self.buffer_flush_size = DEFAULT_BUFFER_FLUSH_SIZE
        self.output_encoding = "utf-8"

    async def _flush_stdout_callback(self, text: str) -> None:
        logger.debug(f"[Daemon:{self.name}]\n{text}")

    async def _flush_stderr_callback(self, text: str) -> None:
        logger.error(f"[Daemon:{self.name}]\n{text}")

    def _stdout_callback(self, data: bytes) -> None:
        self.buffer_stdout.write(data)
        if self.buffer_stdout.tell() >= self.buffer_flush_size:
            text = _flush_buffer(self.buffer_stdout, self.output_encoding)
            run_coroutine_threadsafe(self._flush_stdout_callback(text), self.loop)

    def _stderr_callback(self, data: bytes) -> None:
        self.buffer_stderr.write(data)
        if self.buffer_stderr.tell() >= self.buffer_flush_size:
            text = _flush_buffer(self.buffer_stderr, self.output_encoding)
            run_coroutine_threadsafe(self._flush_stderr_callback(text), self.loop)

    async def install_requirements(
        self, prev_requirements_sha256: Optional[str] = None
    ) -> str:
        if self.requirements_sha256 and prev_requirements_sha256 is not None:
            if prev_requirements_sha256 == self.requirements_sha256:
                logger.debug("The requirements file has not changed")
                return self.requirements_sha256

        await self.venv.create_if_not_exists()

        py_for_pip = self.venv.create_python_subprocess()
        proc = await py_for_pip.start_pip(
            "-r",
            self.requirements_path,
            stdout_callback=self._stdout_callback,
            stderr_callback=self._stderr_callback,
            writable=False,
        )

        text_stdout = _flush_buffer(self.buffer_stdout, self.output_encoding)
        await self._flush_stdout_callback(text_stdout)
        text_stderr = _flush_buffer(self.buffer_stderr, self.output_encoding)
        await self._flush_stderr_callback(text_stderr)

        pip_exit_code = await proc.wait()
        if pip_exit_code != 0:
            raise RuntimeError(f"PIP Installation failed: {pip_exit_code}")

        return self.requirements_sha256

    def is_opened(self) -> bool:
        return self.process is not None

    async def open(self, address: str) -> None:
        if self.process is not None:
            raise RuntimeError("Already process.")

        # [WARNING] Do not use the `self.venv.create_python_subprocess()`
        python_for_daemon = AsyncPythonSubprocess.create_system()

        self.process = await python_for_daemon.start_python(
            "-m",
            "recc",
            "daemon",
            "--daemon-address",
            address,
            "--daemon-file",
            self.script_path,
            "--daemon-packages-dir",
            self.venv.site_packages_dir,
            stdout_callback=self._stdout_callback,
            stderr_callback=self._stderr_callback,
            writable=False,
        )
        self.client = create_daemon_client(address)

    async def close(self) -> None:
        if self.process is None:
            raise RuntimeError("Not exists process.")

        assert self.client is not None
        await self.client.close()
        self.client = None

        self.process.send_signal(SIGINT)
        await self.process.wait()

        text = _flush_buffer(self.buffer_stdout, self.output_encoding)
        await self._flush_stdout_callback(text)
        text = _flush_buffer(self.buffer_stderr, self.output_encoding)
        await self._flush_stderr_callback(text)

        self.process = None
