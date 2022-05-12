# -*- coding: utf-8 -*-

import os
from asyncio import (
    Task,
    create_subprocess_exec,
    create_subprocess_shell,
    create_task,
    gather,
)
from asyncio.streams import StreamReader, StreamWriter
from asyncio.subprocess import PIPE, Process
from enum import Enum
from functools import reduce
from io import BytesIO
from typing import Callable, Mapping, Optional, Tuple

import psutil

from recc.system.environ import get_os_envs_dict

ReaderCallable = Callable[[bytes], None]


class SubprocessMethod(Enum):
    Exec = 0
    Shell = 1


# class SubprocessStatus(Enum):
#     STATUS_RUNNING
#     STATUS_SLEEPING
#     STATUS_DISK_SLEEP
#     STATUS_STOPPED
#     STATUS_TRACING_STOP
#     STATUS_ZOMBIE
#     STATUS_DEAD
#     STATUS_WAKE_KILL
#     STATUS_WAKING
#     STATUS_PARKED(Linux)
#     STATUS_IDLE(Linux, macOS, FreeBSD)
#     STATUS_LOCKED(FreeBSD)
#     STATUS_WAITING(FreeBSD)
#     STATUS_SUSPENDED(NetBSD)


class AsyncSubprocess:
    def __init__(
        self,
        *commands,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
        cwd: Optional[str] = None,
        env: Optional[Mapping[str, str]] = None,
        writable=False,
        method=SubprocessMethod.Exec,
    ):
        self._commands = commands
        self._stdout_callback = stdout_callback
        self._stderr_callback = stderr_callback
        self._writable = writable

        self._process: Optional[Process] = None
        self._stdout_task: Optional[Task] = None
        self._stderr_task: Optional[Task] = None
        self._method = method
        self._cwd = cwd if cwd else os.getcwd()
        self._env = dict(env) if env is not None else get_os_envs_dict()

    def is_started(self) -> bool:
        return self._process is not None

    @staticmethod
    async def _reader(reader: StreamReader, callback: ReaderCallable) -> None:
        while not reader.at_eof():
            buffer = await reader.readline()
            callback(buffer)

    @property
    def stdin_flag(self) -> Optional[int]:
        return PIPE if self._writable else None

    @property
    def stdout_flag(self) -> Optional[int]:
        return PIPE if self._stdout_callback else None

    @property
    def stderr_flag(self) -> Optional[int]:
        return PIPE if self._stderr_callback else None

    async def _create_subprocess_exec(self):
        """
        DeprecationWarning:
        The `loop` argument is deprecated since Python 3.8
        and scheduled for removal in Python 3.10
        """
        return await create_subprocess_exec(
            self._commands[0],
            *self._commands[1:],
            stdin=self.stdin_flag,
            stdout=self.stdout_flag,
            stderr=self.stderr_flag,
            executable=None,
            cwd=self._cwd,
            env=self._env,
        )

    async def _create_subprocess_shell(self) -> Process:
        total_commands = [f"'{str(c).strip()}'" for c in self._commands]
        merged_commands = reduce(lambda x, y: f"{x} {y}", total_commands[1:])

        """
        DeprecationWarning:
        The `loop` argument is deprecated since Python 3.8
        and scheduled for removal in Python 3.10
        """
        return await create_subprocess_shell(
            merged_commands,
            stdin=self.stdin_flag,
            stdout=self.stdout_flag,
            stderr=self.stderr_flag,
            executable=None,
            cwd=self._cwd,
            env=self._env,
        )

    async def create_subprocess(self) -> Process:
        if self._method == SubprocessMethod.Exec:
            return await self._create_subprocess_exec()
        elif self._method == SubprocessMethod.Shell:
            return await self._create_subprocess_shell()
        else:
            raise NotImplementedError

    async def start(self) -> None:
        if self._process is not None:
            raise RuntimeError("Already started process")

        self._process = await self.create_subprocess()

        if self.stdout_flag:
            assert self._process.stdout is not None
            assert self._stdout_callback is not None
            self._stdout_task = create_task(
                self._reader(self._process.stdout, self._stdout_callback)
            )

        if self.stderr_flag:
            assert self._process.stderr is not None
            assert self._stderr_callback is not None
            self._stderr_task = create_task(
                self._reader(self._process.stderr, self._stderr_callback)
            )

    @property
    def process(self) -> Process:
        if not self._process:
            raise RuntimeError("Process is not started")
        return self._process

    @property
    def stdin(self) -> StreamWriter:
        if not self._process:
            raise RuntimeError("Process is not started")
        if not self._writable:
            raise RuntimeError("The writable flag is disabled")
        assert self._process.stdin
        return self._process.stdin

    def write(self, data: bytes) -> None:
        self.stdin.write(data)

    def writelines(self, data) -> None:
        self.stdin.writelines(data)

    def write_eof(self) -> None:
        self.stdin.write_eof()

    def can_write_eof(self) -> bool:
        return self.stdin.can_write_eof()

    def close_stdin(self) -> None:
        self.stdin.close()

    def is_closing_stdin(self) -> bool:
        return self.stdin.is_closing()

    async def wait_closed_stdin(self) -> None:
        await self.stdin.wait_closed()

    async def drain_stdin(self) -> None:
        await self.stdin.drain()

    async def wait_process(self) -> int:
        return await self.process.wait()

    async def wait_callbacks(self) -> None:
        futures = list()
        if self._stdout_task:
            futures.append(self._stdout_task)
        if self._stderr_task:
            futures.append(self._stderr_task)
        await gather(*futures)

    async def wait(self) -> int:
        exit_code = await self.wait_process()
        await self.wait_callbacks()
        return exit_code

    def send_signal(self, signal) -> None:
        self.process.send_signal(signal)

    def terminate(self) -> None:
        self.process.terminate()

    def kill(self) -> None:
        self.process.kill()

    def get_pid(self) -> int:
        return self.process.pid

    # noinspection PyTypeChecker
    @property
    def status(self) -> str:
        return psutil.Process(self.process.pid).status()
        # psutil.STATUS_RUNNING
        # psutil.STATUS_SLEEPING
        # psutil.STATUS_DISK_SLEEP
        # psutil.STATUS_STOPPED
        # psutil.STATUS_TRACING_STOP
        # psutil.STATUS_ZOMBIE
        # psutil.STATUS_DEAD
        # psutil.STATUS_WAKE_KILL
        # psutil.STATUS_WAKING
        # psutil.STATUS_PARKED(Linux)
        # psutil.STATUS_IDLE(Linux, macOS, FreeBSD)
        # psutil.STATUS_LOCKED(FreeBSD)
        # psutil.STATUS_WAITING(FreeBSD)
        # psutil.STATUS_SUSPENDED(NetBSD)

    def is_running(self) -> bool:
        return self.status == psutil.STATUS_RUNNING


async def start_async_subprocess(
    *commands,
    stdout_callback: Optional[ReaderCallable] = None,
    stderr_callback: Optional[ReaderCallable] = None,
    cwd: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
    writable=False,
    method=SubprocessMethod.Exec,
) -> AsyncSubprocess:
    proc = AsyncSubprocess(
        *commands,
        stdout_callback=stdout_callback,
        stderr_callback=stderr_callback,
        cwd=cwd,
        env=env,
        writable=writable,
        method=method,
    )
    await proc.start()
    return proc


async def start_async_subprocess_simply(
    *commands,
    cwd: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
    writable=False,
    method=SubprocessMethod.Exec,
) -> Tuple[int, bytes, bytes]:
    stdout = BytesIO()
    stderr = BytesIO()

    def _stdout_callback(data: bytes) -> None:
        stdout.write(data)

    def _stderr_callback(data: bytes) -> None:
        stderr.write(data)

    proc = await start_async_subprocess(
        *commands,
        stdout_callback=_stdout_callback,
        stderr_callback=_stderr_callback,
        cwd=cwd,
        env=env,
        writable=writable,
        method=method,
    )
    exit_code = await proc.wait()
    return exit_code, stdout.getvalue(), stderr.getvalue()
