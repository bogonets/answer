# -*- coding: utf-8 -*-

from enum import Enum
from asyncio import (
    Task,
    create_task,
    gather,
    create_subprocess_exec,
    create_subprocess_shell,
)
from asyncio.subprocess import Process, PIPE
from asyncio.streams import StreamReader, StreamWriter
from typing import Optional, Callable
from functools import reduce
from recc.exception.recc_error import (
    ReccNotReadyError,
    ReccNoWritableError,
    ReccAlreadyError,
)

ReaderCallable = Callable[[bytes], None]


class SubprocessMethod(Enum):
    Exec = 0
    Shell = 1


class AsyncSubprocess:
    def __init__(
        self,
        *commands,
        stdout_callback: Optional[ReaderCallable] = None,
        stderr_callback: Optional[ReaderCallable] = None,
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
            raise ReccAlreadyError("Already started process.")

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
            raise ReccNotReadyError("Process is not started.")
        return self._process

    @property
    def stdin(self) -> StreamWriter:
        if not self._process:
            raise ReccNotReadyError("Process is not started.")
        if not self._writable:
            raise ReccNoWritableError("The writable flag is disabled.")
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


async def start_async_subprocess(
    *commands,
    stdout_callback: Optional[ReaderCallable] = None,
    stderr_callback: Optional[ReaderCallable] = None,
    writable=False,
) -> AsyncSubprocess:
    proc = AsyncSubprocess(
        *commands,
        stdout_callback=stdout_callback,
        stderr_callback=stderr_callback,
        writable=writable,
    )
    await proc.start()
    return proc
