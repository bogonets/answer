# -*- coding: utf-8 -*-

import os
from abc import ABCMeta, abstractmethod
from asyncio import AbstractEventLoop, gather
from logging import INFO, WARNING, Logger, getLogger
from re import Pattern
from typing import Dict, Iterable, Optional, Sequence, Union

from overrides import overrides

from recc.daemon.daemon_runner import DaemonRunner, DaemonRunnerCallbacks
from recc.daemon.daemon_servicer import wait_connectable
from recc.filesystem.permission import (
    prepare_writable_directory,
    test_writable_directory,
)
from recc.logging.logging import LOGGER_NAME_RECC_DAEMON
from recc.logging.logging import recc_daemon_logger as logger
from recc.package.package_utils import filter_module_names
from recc.packet.daemon import DaemonState


class _RunnerCallback(DaemonRunnerCallbacks):
    def __init__(self, manager: "DaemonManager", slug: str):
        self._manager = manager
        self._slug = slug

    @overrides
    def on_stdout(self, data: bytes) -> None:
        self._manager.on_stdout(self._slug, data)

    @overrides
    def on_stderr(self, data: bytes) -> None:
        self._manager.on_stderr(self._slug, data)

    @overrides
    async def on_exit(self, code: int) -> None:
        await self._manager.on_exit(self._slug, code)


class DaemonManagerEvents(metaclass=ABCMeta):
    @abstractmethod
    def on_stdout(self, slug: str, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_stderr(self, slug: str, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_exit(self, slug: str, code: int) -> None:
        raise NotImplementedError


class DaemonManager(DaemonManagerEvents):
    def __init__(
        self,
        prefix: str,
        working_root_dir: str,
        enable_default_logging=True,
        logging_encoding="utf-8",
        stdout_level=INFO,
        stderr_level=WARNING,
        packages_dirs: Optional[Iterable[str]] = None,
        *,
        connection_retry_delay=1.0,
        connection_max_attempts=5,
        connection_heartbeat_timeout=5.0,
        loop: Optional[AbstractEventLoop] = None,
        denies: Optional[Sequence[Union[str, Pattern]]] = None,
        allows: Optional[Sequence[Union[str, Pattern]]] = None,
    ):
        test_writable_directory(working_root_dir)

        self._modules = filter_module_names(
            prefix=prefix,
            denies=denies,
            allows=allows,
        )
        self._working_root_dir = working_root_dir
        self._enable_default_logging = enable_default_logging
        self._logging_encoding = logging_encoding
        self._stdout_level = stdout_level
        self._stderr_level = stderr_level
        self._packages_dirs = list(packages_dirs) if packages_dirs else list()
        self._connection_retry_delay = connection_retry_delay
        self._connection_max_attempts = connection_max_attempts
        self._connection_heartbeat_timeout = connection_heartbeat_timeout
        self._loop = loop

        self._daemons: Dict[str, DaemonRunner] = dict()
        self._zombies: Dict[str, DaemonRunner] = dict()
        self._loggers: Dict[str, Logger] = dict()

        logger.debug(f"Daemon manager working root: '{working_root_dir}'")
        logger.debug(f"Daemon manager packages dirs: {packages_dirs}")
        logger.debug(f"Daemon plugin prefix: '{prefix}'")
        logger.debug(f"Daemon plugin denies: {denies}")
        logger.debug(f"Daemon plugin allows: {allows}")
        logger.debug(f"Found the daemon plugins: {self._modules}")

    def __len__(self) -> int:
        return len(self._daemons)

    def __contains__(self, slug: str) -> bool:
        return slug in self._daemons

    @property
    def zombies(self):
        return self._zombies

    def get_state(self, slug: str) -> DaemonState:
        try:
            return self._daemons[slug].state
        except KeyError:
            return DaemonState.Unregistered
        except:  # noqa
            return DaemonState.Unknown

    def is_running(self, slug: str) -> bool:
        return self._daemons[slug].running

    def create(self, slug: str, module: str) -> None:
        if not slug:
            raise ValueError("The `slug` of the daemon must exist")
        if not module:
            raise ValueError("The `module` of the daemon must exist")

        if slug in self._daemons:
            raise KeyError(f"The `{slug}` daemon already exists")
        if module not in self._modules:
            raise KeyError(f"Not found module name: {module}")

        working_dir = os.path.join(self._working_root_dir, slug)
        prepare_writable_directory(working_dir)

        self._daemons[slug] = DaemonRunner(
            module_name=module,
            working_dir=working_dir,
            packages_dirs=self._packages_dirs,
            callbacks=_RunnerCallback(self, slug),
        )
        self._loggers[slug] = getLogger(LOGGER_NAME_RECC_DAEMON + "." + slug)

    async def start(self, slug: str, address: str) -> None:
        await self._daemons[slug].start(address, loop=self._loop)
        logger.info(f"The `{slug}` daemon start: {address}")

    async def test_unreachable(self, address: str) -> bool:
        return await wait_connectable(
            address=address,
            retry_delay=self._connection_retry_delay,
            max_attempts=self._connection_max_attempts,
            heartbeat_timeout=self._connection_heartbeat_timeout,
        )

    async def run(
        self,
        slug: str,
        module: str,
        address: str,
        connectable_address: Optional[str] = None,
    ) -> None:
        self.create(slug, module)

        assert slug in self._daemons
        assert slug in self._loggers
        await self.start(slug, address)

        if connectable_address:
            if not await self.test_unreachable(connectable_address):
                raise TimeoutError(f"Unreachable `{slug}` daemon")

    def interrupt(self, slug: str) -> None:
        self._daemons[slug].interrupt()

    def kill(self, slug: str) -> None:
        self._daemons[slug].kill()

    async def close(self, each_join_timeout: Optional[float] = None) -> None:
        if not self._daemons:
            return

        daemons = self._daemons
        self._daemons = dict()

        logger.debug(f"Closing {len(daemons)} daemons ...")

        interrupt_joins = list()
        for slug, daemon in daemons.items():
            if daemon.running:
                logger.debug(f"Send an INTERRUPT signal to `{slug}` daemon")
                daemon.interrupt()
                interrupt_joins.append(daemon.join(each_join_timeout))
        if interrupt_joins:
            logger.debug(f"Joining {len(interrupt_joins)} interrupted daemons ...")
            await gather(*interrupt_joins)

        # Check for non-terminating daemons.
        kill_joins = list()
        for slug, daemon in daemons.items():
            if daemon.running:
                logger.warning(f"Send a KILL signal to `{slug}` daemon")
                daemon.kill()
                kill_joins.append(daemon.join(each_join_timeout))
        if kill_joins:
            logger.warning(f"Joining {len(kill_joins)} killed daemons ...")
            await gather(*kill_joins)

        zombies = dict()
        for slug, daemon in daemons.items():
            if daemon.running:
                zombies[slug] = daemon
                logger.error(f"Still alive `{slug}` daemon")

        self._zombies = zombies
        if zombies:
            logger.error(f"{len(zombies)} zombie daemons have been spawned")

    @overrides
    def on_stdout(self, slug: str, data: bytes) -> None:
        if not self._enable_default_logging:
            return
        message = str(data, encoding=self._logging_encoding).rstrip()
        self._loggers[slug].log(self._stdout_level, message)

    @overrides
    def on_stderr(self, slug: str, data: bytes) -> None:
        if not self._enable_default_logging:
            return
        message = str(data, encoding=self._logging_encoding).rstrip()
        self._loggers[slug].log(self._stderr_level, message)

    @overrides
    async def on_exit(self, slug: str, code: int) -> None:
        if not self._enable_default_logging:
            return

        if code == 0:
            message = f"The `{slug}` daemon exited normally"
            self._loggers[slug].log(self._stdout_level, message)
        else:
            message = f"The `{slug}` daemon exited abnormally {code}"
            self._loggers[slug].log(self._stderr_level, message)
