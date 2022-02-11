# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop
from typing import Optional
from recc.argparse.config.core_config import CoreConfig
from recc.logging.logging import recc_core_logger as logger
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.core.mixin.context_config import ContextConfig
from recc.core.mixin.context_daemon import ContextDaemon
from recc.core.mixin.context_group import ContextGroup
from recc.core.mixin.context_info import ContextInfo
from recc.core.mixin.context_init import ContextInit
from recc.core.mixin.context_lamda import ContextLamda
from recc.core.mixin.context_layout import ContextLayout
from recc.core.mixin.context_plugin import ContextPlugin
from recc.core.mixin.context_port import ContextPort
from recc.core.mixin.context_project import ContextProject
from recc.core.mixin.context_role import ContextRole
from recc.core.mixin.context_storage import ContextStorage
from recc.core.mixin.context_system import ContextSystem
from recc.core.mixin.context_task import ContextTask
from recc.core.mixin.context_user import ContextUser
from recc.util.version import (
    version_text,
    version_info,
    database_version,
    database_info,
)
from recc.variables.database import (
    CONFIG_PREFIX_RECC_ARGPARSE_CONFIG,
    ROLE_UID_OWNER,
    ROLE_SLUG_OWNER,
)


class Context(
    ContextConfig,
    ContextDaemon,
    ContextGroup,
    ContextInfo,
    ContextInit,
    ContextLamda,
    ContextLayout,
    ContextPlugin,
    ContextPort,
    ContextProject,
    ContextRole,
    ContextStorage,
    ContextSystem,
    ContextTask,
    ContextUser,
):
    """
    Core context.
    """

    _closed: bool

    def __init__(
        self,
        config: Optional[CoreConfig] = None,
        *,
        loop: Optional[AbstractEventLoop] = None,
        skip_assertion: Optional[bool] = None,
    ):
        self._closed = True
        self.init_all(config, loop, skip_assertion)

    @classmethod
    def version_text(cls) -> str:
        return version_text

    @classmethod
    def version_info(cls) -> tuple:
        return version_info

    @classmethod
    def database_version(cls) -> str:
        return database_version

    @classmethod
    def database_info(cls) -> tuple:
        return database_info

    @staticmethod
    async def _test_recc_subprocess() -> None:
        try:
            python = AsyncPythonSubprocess.create_system()
            version = await python.recc_version()
            logger.info(f"The `recc` module version is {version}.")
        except BaseException as e:
            logger.warning(
                "Could not find module `recc`. "
                "Some functions that run as subprocesses are not available. "
                f"{e}"
            )

    async def open(self) -> None:
        await self._test_recc_subprocess()

        self.setup_context_config()
        logger.info("Setup context configurations")

        await self._database.open()
        logger.info("Opened database")

        await self._database.create_tables()
        logger.info("Create tables (if not exists)")

        owner_uid = await self._database.select_role_uid_by_slug(ROLE_SLUG_OWNER)
        if owner_uid != ROLE_UID_OWNER:
            logger.critical(
                f"Owner role ID is not {ROLE_UID_OWNER}, It's actually {owner_uid}"
            )
            raise RuntimeError(f"The owner role ID must be {ROLE_UID_OWNER}")

        assert self._database.is_open()
        config_infos_prefix = CONFIG_PREFIX_RECC_ARGPARSE_CONFIG
        config_infos = await self.get_infos_like(config_infos_prefix + "%")
        database_configs = {c.key: c.value for c in config_infos if c.key and c.value}
        await self.restore_configs(database_configs)
        logger.info("Restores the configuration from the database")

        await self._container.open()
        logger.info("Opened container-manager")

        assert self._container.is_open()
        image_validate = self._config.container_image_validate
        if not await self._container.exist_default_task_images(image_validate):
            logger.info("Create default-task-image ...")
            try:
                await self._container.create_default_task_images()
            except Exception as e:
                logger.exception(e)
            else:
                logger.info("Default-task-image successfully created.")

        if self.is_guest_mode():
            await self.connect_global_network()
            logger.info("Connect global network.")

        await self._cache.open()
        logger.info("Opened cache-store")

        await self._tasks.open()
        logger.info("Opened task-manager")

        await self._daemons.open(self._storage.daemon, self.database, self._loop)
        logger.info("Opened daemon-manager")

        await self._daemons.register()
        logger.info("Init daemon-manager")

        await self._plugins.open()
        logger.info("Opened plugin-manager")

        await self._after_open()
        logger.info("The context has been opened")

    async def _after_open(self) -> None:
        assert len(self.ports.alloc_ports) == 0
        await self.update_ports_from_database()
        database_ports = len(self.ports.alloc_ports)
        logger.info(f"Number of ports allocated from database: {database_ports}")

        await self.update_ports_from_container()
        container_ports = len(self.ports.alloc_ports) - database_ports
        logger.info(f"Number of ports allocated from container: {container_ports}")

        if self.config.developer:
            logger.debug(f"Allocated ports: {list(self.ports.alloc_ports)}")

    async def _before_close(self) -> None:
        await self._daemons.close()
        logger.info("Daemon-manager de-initialization is complete")

        if self.container.is_open() and self.is_guest_mode():
            await self.disconnect_global_network()
            logger.info("Disconnect global network")

    async def close(self) -> None:
        logger.info("Closing the context")
        await self._before_close()

        teardown = self._config.teardown

        await self._plugins.close()
        logger.info("Closed plugin-manager")

        self._plugins.destroy()
        logger.info("Destroyed plugin-manager")

        await self._tasks.close()
        logger.info("Closed task-manager")

        if teardown:
            await self._cache.clear()
            logger.info("Clear caches")

        await self._cache.close()
        logger.info("Closed cache-store")

        await self._container.close()
        logger.info("Closed container-manager")

        if teardown:
            await self._database.drop_tables()
            logger.info("Drop tables")

        await self._database.close()
        logger.info("Closed database")
