# -*- coding: utf-8 -*-

import os
import sys
from signal import SIGINT
from abc import ABCMeta, abstractmethod
from typing import Optional, List
from re import Pattern
from re import compile as re_compile
from functools import partial
from asyncio import (
    AbstractEventLoop,
    run_coroutine_threadsafe,
    Task,
    wait_for,
    shield,
    get_running_loop,
    gather,
)
from overrides import overrides
from recc.subprocess.async_subprocess import AsyncSubprocess
from recc.subprocess.async_python_subprocess import (
    Package,
    PackageInfo,
    AsyncPythonSubprocess,
)
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc.argparse.config.global_config import ARG_LOG_SIMPLY
from recc.argparse.command import Command
from recc.argparse.config.daemon_config import (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_SCRIPT,
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

RE_REQUIREMENTS = re_compile(r"requirements.*\.txt")
RE_CONSTRAINTS = re_compile(r"constraints.*\.txt")


class DaemonRunnerCallbacks(metaclass=ABCMeta):
    @abstractmethod
    async def on_created_venv(self, root: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_stdout(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_stderr(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_daemon_done(self, exit_code: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_pip_install_stdout(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_pip_install_stderr(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_pip_install_done(self, exit_code: int) -> None:
        raise NotImplementedError


class StandardDaemonRunnerCallbacks(DaemonRunnerCallbacks):
    @overrides
    async def on_created_venv(self, root: str) -> None:
        sys.stdout.write(f"The virtual environment has been created: '{root}'\n")

    @overrides
    async def on_stdout(self, data: bytes) -> None:
        sys.stdout.write(str(data, encoding="utf-8"))

    @overrides
    async def on_stderr(self, data: bytes) -> None:
        sys.stderr.write(str(data, encoding="utf-8"))

    @overrides
    async def on_daemon_done(self, exit_code: int) -> None:
        report = f"Daemon process done (exit_code={exit_code})\n"
        if exit_code == 0:
            sys.stdout.write(report)
        else:
            sys.stderr.write(report)

    @overrides
    async def on_pip_install_stdout(self, data: bytes) -> None:
        sys.stdout.write(str(data, encoding="utf-8"))

    @overrides
    async def on_pip_install_stderr(self, data: bytes) -> None:
        sys.stderr.write(str(data, encoding="utf-8"))

    @overrides
    async def on_pip_install_done(self, exit_code: int) -> None:
        report = f"pip install done (exit_code={exit_code})\n"
        if exit_code == 0:
            sys.stdout.write(report)
        else:
            sys.stderr.write(report)


class DaemonRunner:
    def __init__(
        self,
        plugin_dir: str,
        plugin_script_path: str,
        work_dir: str,
        venv_dir: str,
        system_site_packages=False,
        pip_timeout: Optional[float] = None,
        callbacks: Optional[DaemonRunnerCallbacks] = None,
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

        self._venv_task: Optional[Task] = None

        self._daemon_process: Optional[AsyncSubprocess] = None
        self._daemon_task: Optional[Task] = None

        self._pip_process: Optional[AsyncSubprocess] = None
        self._pip_task: Optional[Task] = None

        self._callbacks = callbacks

    @staticmethod
    async def _timeout_wrapper(coro, timeout: Optional[float] = None) -> None:
        if timeout is not None:
            assert timeout > 0
            await wait_for(coro, timeout=timeout)
        else:
            await coro

    @staticmethod
    async def _cancel_task(task: Optional[Task]) -> None:
        if task is None:
            return
        if task.done():
            return
        task.cancel()
        try:
            await task
        except:  # noqa
            pass

    @staticmethod
    async def _join_task(task: Optional[Task], timeout: Optional[float] = None) -> None:
        if task is None:
            return
        if timeout is not None:
            assert timeout > 0
            await wait_for(shield(task), timeout=timeout)
        else:
            await task

    async def cancel_venv_task(self) -> None:
        await self._cancel_task(self._venv_task)

    async def join_venv_task(self, timeout: Optional[float] = None) -> None:
        await self._join_task(self._venv_task, timeout)

    async def cancel_daemon_task(self) -> None:
        await self._cancel_task(self._daemon_task)

    async def join_daemon_task(self, timeout: Optional[float] = None) -> None:
        await self._join_task(self._daemon_task, timeout)

    async def cancel_pip_task(self) -> None:
        await self._cancel_task(self._pip_task)

    async def join_pip_task(self, timeout: Optional[float] = None) -> None:
        await self._join_task(self._pip_task, timeout)

    async def create_venv(
        self,
        timeout: Optional[float] = None,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        if self._venv_task is not None:
            raise RuntimeError("Already creating virtual environment")

        running_loop = loop if loop else get_running_loop()
        self._venv_task = running_loop.create_task(
            self._timeout_wrapper(self._venv.create_if_not_exists(), timeout)
        )
        self._venv_task.add_done_callback(partial(self._venv_task_done, running_loop))

    def _venv_task_done(self, loop: AbstractEventLoop, task: Task) -> None:
        assert self._venv_task == task
        self._venv_task = None
        if self._callbacks is None:
            return
        run_coroutine_threadsafe(self._callbacks.on_created_venv(self.venv_dir), loop)

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
        if self._venv_task is not None:
            if not self._venv_task.done():
                return DaemonState.EnvCreating

        if not self.exists:
            return DaemonState.EnvNotFound

        if self._daemon_process is None:
            return DaemonState.Down

        return DaemonState.from_process_status(self._daemon_process.status)

    def is_venv_creating(self) -> bool:
        return self._venv_task is not None and not self._venv_task.done()

    def is_daemon_running(self) -> bool:
        return self._daemon_task is not None and not self._daemon_task.done()

    def is_pip_running(self) -> bool:
        return self._pip_task is not None and not self._pip_task.done()

    def _stdout_callback(self, loop: AbstractEventLoop, data: bytes) -> None:
        if self._callbacks is None:
            return
        run_coroutine_threadsafe(self._callbacks.on_stdout(data), loop)

    def _stderr_callback(self, loop: AbstractEventLoop, data: bytes) -> None:
        if self._callbacks is None:
            return
        run_coroutine_threadsafe(self._callbacks.on_stderr(data), loop)

    async def start_daemon(
        self,
        address: str,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        if self._daemon_task is not None:
            raise RuntimeError("Already daemon task")

        if self._daemon_process is not None:
            pid = self._daemon_process.get_pid()
            raise RuntimeError(f"Already daemon process (pid={pid})")

        # [IMPORTANT]
        # Do not use the `self._venv.create_python_subprocess()`
        # After running the already installed daemon-server of `recc`,
        # the daemon plugin is executed.
        python_for_daemon = AsyncPythonSubprocess.create_system()

        subcommands = [
            "-m",
            "recc",
            ARG_LOG_SIMPLY.long_key,
            Command.daemon.name,
            ARG_DAEMON_ADDRESS.long_key,
            address,
            ARG_DAEMON_SCRIPT.long_key,
            self._plugin_script_path,
            ARG_DAEMON_PACKAGES_DIR.long_key,
            self._venv.site_packages_dir,
        ]

        running_loop = loop if loop else get_running_loop()
        self._daemon_process = await python_for_daemon.start_python(
            *subcommands,
            stdout_callback=partial(self._stdout_callback, running_loop),
            stderr_callback=partial(self._stderr_callback, running_loop),
            cwd=self._work_dir,
            writable=False,
        )

        self._daemon_task = running_loop.create_task(self._daemon_process.wait())
        self._daemon_task.add_done_callback(
            partial(self._daemon_task_done, running_loop)
        )

    def _daemon_task_done(self, loop: AbstractEventLoop, task: Task) -> None:
        assert self._daemon_task is not None
        assert self._daemon_process is not None
        assert self._daemon_task == task

        exit_code = self._daemon_task.result()
        assert isinstance(exit_code, int)

        self._daemon_task = None
        self._daemon_process = None

        if self._callbacks is None:
            return

        run_coroutine_threadsafe(self._callbacks.on_daemon_done(exit_code), loop)

    async def interrupt_daemon(self) -> None:
        if self._daemon_process is None:
            raise RuntimeError("Not exists daemon process")
        self._daemon_process.send_signal(SIGINT)

    async def kill_daemon(self) -> None:
        if self._daemon_process is None:
            raise RuntimeError("Not exists daemon process")
        self._daemon_process.kill()

    async def list_pip(self) -> List[Package]:
        return await self._venv.create_python_subprocess().list()

    async def show_pip(self, package: str) -> PackageInfo:
        return await self._venv.create_python_subprocess().show_as_info(package)

    async def uninstall_pip(self, package: str) -> int:
        return await self._venv.create_python_subprocess().uninstall(package)

    def _pip_install_stdout_callback(
        self, loop: AbstractEventLoop, data: bytes
    ) -> None:
        if self._callbacks is None:
            return
        run_coroutine_threadsafe(self._callbacks.on_pip_install_stdout(data), loop)

    def _pip_install_stderr_callback(
        self, loop: AbstractEventLoop, data: bytes
    ) -> None:
        if self._callbacks is None:
            return
        run_coroutine_threadsafe(self._callbacks.on_pip_install_stderr(data), loop)

    async def install_pip(
        self,
        *arguments: str,
        upgrade=False,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        if self._pip_task is not None:
            raise RuntimeError("Already pip task")

        if self._pip_process is not None:
            pid = self._pip_process.get_pid()
            raise RuntimeError(f"Already pip process (pid={pid})")

        python_for_pip = self._venv.create_python_subprocess()
        subcommands = ["install", "--progress-bar=ascii"]
        if upgrade:
            subcommands.append("--upgrade")
        subcommands += arguments

        running_loop = loop if loop else get_running_loop()
        self._pip_process = await python_for_pip.start_pip(
            *subcommands,
            stdout_callback=partial(self._pip_install_stdout_callback, running_loop),
            stderr_callback=partial(self._pip_install_stderr_callback, running_loop),
            cwd=self._work_dir,
            env=python_for_pip.env,
            writable=False,
        )

        self._pip_task = running_loop.create_task(self._pip_process.wait())
        self._pip_task.add_done_callback(partial(self._pip_task_done, running_loop))

    def _pip_task_done(self, loop: AbstractEventLoop, task: Task) -> None:
        assert self._pip_task is not None
        assert self._pip_process is not None
        assert self._pip_task == task

        exit_code = self._pip_task.result()
        assert isinstance(exit_code, int)

        self._pip_task = None
        self._pip_process = None

        if self._callbacks is None:
            return

        run_coroutine_threadsafe(self._callbacks.on_pip_install_done(exit_code), loop)

    async def interrupt_pip(self) -> None:
        if self._pip_process is None:
            raise RuntimeError("Not exists pip process")
        self._pip_process.send_signal(SIGINT)

    async def close(
        self,
        timeout: Optional[float] = None,
    ) -> None:
        joins = list()
        if self.is_venv_creating():
            joins.append(self.join_venv_task(timeout))
        if self.is_daemon_running():
            joins.append(self.join_daemon_task(timeout))
        if self.is_pip_running():
            joins.append(self.join_pip_task(timeout))
        await gather(*joins)

    @staticmethod
    def _find_files(
        directory: str,
        name_pattern: Pattern,
        join_prefix=False,
    ) -> List[str]:
        result = list()
        for name in os.listdir(directory):
            if name_pattern.match(name):
                f = os.path.join(directory, name) if join_prefix else name
                result.append(f)
        return result

    def find_requirements(self, join_dir=False) -> List[str]:
        return self._find_files(self.plugin_dir, RE_REQUIREMENTS, join_dir)

    def find_constraints(self, join_dir=False) -> List[str]:
        return self._find_files(self.plugin_dir, RE_CONSTRAINTS, join_dir)
