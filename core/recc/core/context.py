# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop
from typing import Optional
from recc.argparse.config.core_config import CoreConfig
from recc.log.logging import recc_logger as logger
from recc.core.mixin.context_init import ContextInit
from recc.core.mixin.context_layout import ContextLayout
from recc.core.mixin.context_project import ContextProject
from recc.core.mixin.context_storage import ContextStorage
from recc.core.mixin.context_task import ContextTask
from recc.core.mixin.context_user import ContextUser


class Context(
    ContextInit,
    ContextLayout,
    ContextProject,
    ContextStorage,
    ContextTask,
    ContextUser,
):
    """
    Core context.
    """

    def __init__(
        self,
        config: Optional[CoreConfig] = None,
        *,
        loop: Optional[AbstractEventLoop] = None,
        skip_assertion: Optional[bool] = None,
    ):
        self.init_all(config, loop, skip_assertion)

    async def _after_open(self) -> None:
        if self.cm.is_open() and self.is_guest_mode():
            await self.connect_global_network()

    async def _before_close(self) -> None:
        if self.cm.is_open() and self.is_guest_mode():
            await self.disconnect_global_network()

    async def open(self) -> None:
        await self._db.open()
        logger.info("Opened database")

        await self._db.create_tables()
        logger.info("Create tables (if not exists)")

        await self._db.update_cache()
        logger.info("Updated database cache")

        await self._cm.open()
        logger.info("Opened container-manager")

        await self._cs.open()
        logger.info("Opened cache-store")

        await self._tm.open()
        logger.info("Opened task-manager")

        await self._after_open()
        logger.info("The context has been opened")

    async def close(self) -> None:
        logger.info("Closing the context")
        await self._before_close()

        teardown = self._config.teardown

        await self._tm.close()
        logger.info("Closed task-manager")

        await self._cs.close()
        logger.info("Closed cache-store")

        await self._cm.close()
        logger.info("Closed container-manager")

        if teardown:
            await self._db.drop_tables()
            logger.info("Drop tables")

        await self._db.close()
        logger.info("Closed database")
