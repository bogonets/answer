# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional, List, Dict, Tuple, Mapping
from functools import reduce
from dataclasses import dataclass
from recc.subprocess.async_subprocess import (
    SubprocessMethod,
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


@dataclass
class PackageInfo:
    name: str
    version: str
    summary: str
    homepage: str
    author: str
    author_email: str
    license: str
    location: str
    requires: List[str]
    required_by: List[str]


class AsyncPythonSubprocess:
    def __init__(
        self,
        executable: Optional[str] = None,
        pip_timeout: Optional[float] = None,
        env: Optional[Mapping[str, str]] = None,
        method=SubprocessMethod.Exec,
    ):
        self._executable = executable if executable else sys.executable
        self._pip_timeout = pip_timeout if pip_timeout else 0.0

        self.env = dict(env) if env is not None else dict()
        self.method = method

    @property
    def executable(self) -> str:
        return self._executable

    @property
    def executable_dir(self) -> str:
        return os.path.dirname(self._executable)

    @classmethod
    def create_system(cls, pip_timeout: Optional[float] = None):
        return cls(sys.executable, pip_timeout)

    async def start_python(
        self,
        *subcommands,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
        cwd: Optional[str] = None,
        env: Optional[Mapping[str, str]] = None,
        writable=False,
        method=SubprocessMethod.Exec,
    ) -> AsyncSubprocess:
        if not subcommands:
            ValueError("Empty subcommands arguments")

        total_commands = [self._executable, *subcommands]
        proc = await start_async_subprocess(
            *total_commands,
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
            cwd=cwd,
            env=env,
            writable=writable,
            method=method,
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
        cwd: Optional[str] = None,
        env: Optional[Mapping[str, str]] = None,
        writable=False,
        method=SubprocessMethod.Exec,
    ) -> AsyncSubprocess:
        return await self.start_python(
            *self.make_pip_subcommands(*subcommands),
            stdout_callback=stdout_callback,
            stderr_callback=stderr_callback,
            cwd=cwd,
            env=env,
            writable=writable,
            method=method,
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
            cwd=None,
            env=self.env,
            writable=False,
            method=self.method,
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
            error_msg = f"python {subcommands[0]} error: {params_msg}"
            raise RuntimeError(error_msg)

        return stdout_lines, stderr_lines

    async def start_pip_simply(self, *subcommands) -> Tuple[List[str], List[str]]:
        return await self.start_python_simply(*self.make_pip_subcommands(*subcommands))

    async def ensure_pip(self, isolate=True) -> Tuple[List[str], List[str]]:
        """
        Run ``ensure_pip`` module.

        :param isolate:
            If pydevd is connected, the ``python -Im ensure_pip`` command does not work
            properly. In this case, it is temporarily resolved by using the ``isolate``
            flag as ``False``. If possible, use only for debugging and testing purposes.
        """

        return await self.start_python_simply(
            "-Im" if isolate else "-m",
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

    async def show(self, package: str) -> Dict[str, str]:
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

    async def show_as_info(self, package: str) -> PackageInfo:
        info = await self.show(package)

        def _split_packages(text: str) -> List[str]:
            return list(
                filter(
                    lambda x: bool(x),
                    map(
                        lambda x: x.strip(),
                        text.split(","),
                    ),
                )
            )

        name = info.get("Name", "").strip()
        version = info.get("Version", "").strip()
        summary = info.get("Summary", "").strip()
        homepage = info.get("Home-page", "").strip()
        author = info.get("Author", "").strip()
        author_email = info.get("Author-email", "").strip()
        license_ = info.get("License", "").strip()  # Shadows built-in name 'license'
        location = info.get("Location", "").strip()
        requires = _split_packages(info.get("Requires", ""))
        required_by = _split_packages(info.get("Required-by", ""))

        return PackageInfo(
            name,
            version,
            summary,
            homepage,
            author,
            author_email,
            license_,
            location,
            requires,
            required_by,
        )
