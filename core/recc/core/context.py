# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop
from typing import Optional
from recc.argparse.config.core_config import CoreConfig
from recc.log.logging import recc_core_logger as logger
from recc.core.mixin.context_init import ContextInit
from recc.core.mixin.context_layout import ContextLayout
from recc.core.mixin.context_port import ContextPort
from recc.core.mixin.context_project import ContextProject
from recc.core.mixin.context_storage import ContextStorage
from recc.core.mixin.context_task import ContextTask
from recc.core.mixin.context_user import ContextUser


class Context(
    ContextInit,
    ContextLayout,
    ContextPort,
    ContextProject,
    ContextStorage,
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

    async def open(self) -> None:
        await self._database.open()
        logger.info("Opened database")

        await self._database.create_tables()
        logger.info("Create tables (if not exists)")

        await self._database.update_cache()
        logger.info("Updated database cache")

        await self._container.open()
        logger.info("Opened container-manager")

        assert self._container.is_open()
        if not await self._container.exist_default_task_images(False):
            logger.info("Create default-task-image ...")
            try:
                await self._container.create_default_task_images()
            except Exception as e:
                logger.exception(e)
            else:
                logger.info("Default-task-image successfully created.")

        await self._cache.open()
        logger.info("Opened cache-store")

        await self._tasks.open()
        logger.info("Opened task-manager")

        await self._after_open()
        logger.info("The context has been opened")

    async def _after_open(self) -> None:
        if self.container.is_open() and self.is_guest_mode():
            await self.connect_global_network()
            logger.info("Connect global network.")

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
        if self.container.is_open() and self.is_guest_mode():
            await self.disconnect_global_network()
            logger.info("Disconnect global network.")

    async def close(self) -> None:
        logger.info("Closing the context")
        await self._before_close()

        teardown = self._config.teardown

        await self._tasks.close()
        logger.info("Closed task-manager")

        await self._cache.close()
        logger.info("Closed cache-store")

        await self._container.close()
        logger.info("Closed container-manager")

        if teardown:
            await self._database.drop_tables()
            logger.info("Drop tables")

        await self._database.close()
        logger.info("Closed database")
