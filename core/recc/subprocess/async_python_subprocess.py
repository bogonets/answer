# -*- coding: utf-8 -*-

import sys
from typing import Optional, List, Dict, Tuple
from functools import reduce
from recc.subprocess.async_subprocess import (
    AsyncSubprocess,
    ReaderCallable,
    start_async_subprocess,
)
from recc.driver.json import global_json_decoder


class Package(object):

    __slots__ = ("name", "version")

    name: str
    version: str

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def __str__(self) -> str:
        return f"{self.name}=={self.version}"

    def __repr__(self) -> str:
        return f"Package<name={self.name},version={self.version}>"


class AsyncPythonSubprocess:
    def __init__(
        self,
        python_executable_path: str,
        pip_timeout: Optional[float] = None,
    ):
        self._python_executable_path = python_executable_path
        self._pip_timeout = pip_timeout if pip_timeout else 0.0

    @property
    def executable(self):
        return self._python_executable_path

    @classmethod
    def create_system(cls, pip_timeout: Optional[float] = None):
        return cls(sys.executable, pip_timeout)

    async def start_python(
        self,
        *subcommands,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
        writable=False,
    ) -> AsyncSubprocess:
        if not subcommands:
            ValueError("Empty subcommands arguments")

        total_commands = [self._python_executable_path, *subcommands]
        proc = await start_async_subprocess(
            *total_commands,
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
            writable=writable,
        )
        return proc

    def make_pip_subcommands(self, *subcommands) -> List[str]:
        result = [
            "-m",
            "pip",
            "--no-color",
            "--no-input",
            "--disable-pip-version-check",
            "--no-python-version-warning",
        ]
        if self._pip_timeout > 0.0:
            result += ["--timeout", str(self._pip_timeout)]
        if subcommands:
            result += subcommands
        return result

    async def start_pip(
        self,
        *subcommands,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
        writable=False,
    ) -> AsyncSubprocess:
        return await self.start_python(
            *self.make_pip_subcommands(*subcommands),
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
            writable=writable,
        )

    async def start_python_simply(self, *subcommands) -> Tuple[List[str], List[str]]:
        stdout_lines: List[str] = list()
        stderr_lines: List[str] = list()

        def _stdout_callback(data: bytes) -> None:
            line = str(data, encoding="utf-8").strip()
            if line:
                stdout_lines.append(line)

        def _stderr_callback(data: bytes) -> None:
            line = str(data, encoding="utf-8").strip()
            if line:
                stderr_lines.append(line)

        proc = await self.start_python(
            *subcommands,
            stdout_callback=_stdout_callback,
            stderr_callback=_stderr_callback,
            writable=False,
        )
        exit_code = await proc.wait()

        if exit_code != 0:
            params_msg = f"code={exit_code}"
            if stdout_lines:
                stdout_text = reduce(lambda x, y: f"{x} {y}", stdout_lines)
                params_msg += f",stdout={stdout_text}"
            if stderr_lines:
                stderr_text = reduce(lambda x, y: f"{x} {y}", stderr_lines)
                params_msg += f",stderr={stderr_text}"
            error_msg = f"pip {subcommands[0]} error: {params_msg}"
            raise RuntimeError(error_msg)

        return stdout_lines, stderr_lines

    async def start_pip_simply(self, *subcommands) -> Tuple[List[str], List[str]]:
        return await self.start_python_simply(*self.make_pip_subcommands(*subcommands))

    async def ensure_pip(self) -> Tuple[List[str], List[str]]:
        return await self.start_python_simply(
            "-Im",
            "ensurepip",
            "--upgrade",
            "--default-pip",
        )

    async def recc_version(self) -> str:
        stdout_lines, _ = await self.start_python_simply("-m", "recc", "--version")
        assert len(stdout_lines) == 1
        return stdout_lines[0].strip()

    async def version(self) -> str:
        stdout_lines, _ = await self.start_python_simply("--version")
        assert len(stdout_lines) == 1
        prefix, version = stdout_lines[0].split(" ", 1)
        assert prefix == "Python"
        return version

    async def version_tuple(self) -> Tuple[int, int, int]:
        versions = [int(i) for i in (await self.version()).split(".")]
        assert len(versions) == 3
        return versions[0], versions[1], versions[2]

    async def install(
        self,
        package: str,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
    ) -> int:
        proc = await self.start_pip(
            "install",
            "--progress-bar=ascii",
            package,
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
        )
        return await proc.wait()

    async def upgrade(
        self,
        package: str,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
    ) -> int:
        proc = await self.start_pip(
            "install",
            "--progress-bar=ascii",
            "--upgrade",
            package,
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
        )
        return await proc.wait()

    async def uninstall(
        self,
        package: str,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
    ) -> int:
        proc = await self.start_pip(
            "uninstall",
            "--yes",
            package,
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
        )
        return await proc.wait()

    async def list(self) -> List[Package]:
        stdout_lines, _ = await self.start_pip_simply("list", "--format=json")
        json_text = reduce(lambda x, y: f"{x}{y}", stdout_lines)
        packages = global_json_decoder(json_text)
        return [Package(p["name"], p["version"]) for p in packages]

    async def show(self, package) -> Dict[str, str]:
        stdout_lines, _ = await self.start_pip_simply("show", package)
        result = dict()
        for header_line in stdout_lines:
            # The output is in RFC-compliant mail header format.
            items = header_line.split(":", maxsplit=1)
            assert len(items) == 2
            key = items[0].strip()
            val = items[1].strip()
            result[key] = val
        return result
