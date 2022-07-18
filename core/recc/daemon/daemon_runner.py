# -*- coding: utf-8 -*-

import os
import sys
from abc import ABCMeta, abstractmethod
from asyncio import (
    AbstractEventLoop,
    Task,
    get_running_loop,
    run_coroutine_threadsafe,
    shield,
    wait_for,
)
from functools import partial
from signal import SIGINT
from typing import Iterable, Optional

from overrides import overrides
from psutil import NoSuchProcess

from recc.argparse.command import Command
from recc.argparse.config.daemon_config import (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_MODULE,
    ARG_DAEMON_PACKAGES_DIR,
)
from recc.argparse.config.global_config import ARG_LOG_SIMPLY
from recc.filesystem.permission import is_writable_dir
from recc.packet.daemon import DaemonState
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.subprocess.async_subprocess import AsyncSubprocess


class DaemonRunnerCallbacks(metaclass=ABCMeta):
    @abstractmethod
    def on_stdout(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_stderr(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_exit(self, code: int) -> None:
        raise NotImplementedError


class StandardDaemonRunnerCallbacks(DaemonRunnerCallbacks):
    @overrides
    def on_stdout(self, data: bytes) -> None:
        sys.stdout.write(str(data, encoding="utf-8"))

    @overrides
    def on_stderr(self, data: bytes) -> None:
        sys.stderr.write(str(data, encoding="utf-8"))

    @overrides
    async def on_exit(self, code: int) -> None:
        report = f"The daemon process has been exited (code={code})\n"
        if code == 0:
            sys.stdout.write(report)
        else:
            sys.stderr.write(report)


class DaemonRunner:
    def __init__(
        self,
        module_name: str,
        working_dir: str,
        packages_dirs: Optional[Iterable[str]] = None,
        callbacks: Optional[DaemonRunnerCallbacks] = None,
    ) -> None:
        assert os.path.isdir(working_dir)
        assert is_writable_dir(working_dir)

        self._module_name = module_name
        self._working_dir = working_dir
        self._packages_dirs = list(packages_dirs) if packages_dirs else list()
        self._callbacks = callbacks

        self._process: Optional[AsyncSubprocess] = None
        self._task: Optional[Task] = None

    async def cancel_task(self) -> None:
        if self._task is None:
            return
        if self._task.done():
            return
        self._task.cancel()
        try:
            await self._task
        except:  # noqa
            pass

    async def join(self, timeout: Optional[float] = None) -> None:
        if self._task is None:
            return
        if timeout is not None:
            assert timeout > 0
            await wait_for(shield(self._task), timeout=timeout)
        else:
            await self._task

    @property
    def working(self) -> str:
        return self._working_dir

    @property
    def running(self) -> bool:
        return self._task is not None and not self._task.done()

    @property
    def state(self) -> DaemonState:
        if self._process:
            try:
                return DaemonState.from_process_status(self._process.status)
            except NoSuchProcess:
                return DaemonState.NoSuchProcess
            except:  # noqa
                return DaemonState.Unknown
        else:
            return DaemonState.Down

    def _stdout_callback(self, data: bytes) -> None:
        if self._callbacks is None:
            return
        self._callbacks.on_stdout(data)

    def _stderr_callback(self, data: bytes) -> None:
        if self._callbacks is None:
            return
        self._callbacks.on_stderr(data)

    async def start(
        self,
        address: str,
        *,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        if self._task is not None:
            raise RuntimeError("Already daemon task")

        if self._process is not None:
            pid = self._process.get_pid()
            raise RuntimeError(f"Already daemon process (pid={pid})")

        subcommands = [
            "-m",
            "recc",
            ARG_LOG_SIMPLY.long_key,
            Command.daemon.name,
            ARG_DAEMON_ADDRESS.long_key,
            address,
            ARG_DAEMON_MODULE.long_key,
            self._module_name,
        ]

        for packages_dir in self._packages_dirs:
            subcommands += [ARG_DAEMON_PACKAGES_DIR.long_key, packages_dir]

        running_loop = loop if loop else get_running_loop()
        python = AsyncPythonSubprocess.create_system()
        self._process = await python.start_python(
            *subcommands,
            stdout_callback=self._stdout_callback,
            stderr_callback=self._stderr_callback,
            cwd=self._working_dir,
            writable=False,
        )

        self._task = running_loop.create_task(self._process.wait())
        self._task.add_done_callback(partial(self._on_task_done, running_loop))

    def _on_task_done(self, loop: AbstractEventLoop, task: Task) -> None:
        assert self._task is not None
        assert self._process is not None
        assert self._task == task

        exit_code = self._task.result()
        assert isinstance(exit_code, int)

        self._task = None
        self._process = None

        if self._callbacks is not None:
            run_coroutine_threadsafe(self._callbacks.on_exit(exit_code), loop)

    def interrupt(self) -> None:
        if self._process is None:
            raise RuntimeError("Not exists daemon process")
        self._process.send_signal(SIGINT)

    def kill(self) -> None:
        if self._process is None:
            raise RuntimeError("Not exists daemon process")
        self._process.kill()
