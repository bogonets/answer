# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop, get_event_loop_policy, set_event_loop
from typing import Dict, Optional, Set

from recc_cache import Cache
from recc_database.database.pg_db import PgDb

from recc.config import Config
from recc.core.mixin.context_config import ContextConfig
from recc.core.mixin.context_group import ContextGroup
from recc.core.mixin.context_info import ContextInfo
from recc.core.mixin.context_plugin import ContextPlugin
from recc.core.mixin.context_project import ContextProject
from recc.core.mixin.context_role import ContextRole
from recc.core.mixin.context_system import ContextSystem
from recc.core.mixin.context_user import ContextUser
from recc.crypto.signature import generate_signature
from recc.init.default import init_logger
from recc.logging.logging import recc_core_logger as logger
from recc.plugin.core_plugin_manager import CorePluginManager
from recc.session.session import (
    DEFAULT_ACCESS_MAX_AGE_SECONDS,
    DEFAULT_ISSUER_RECC_ACCESS,
    DEFAULT_ISSUER_RECC_REFRESH,
    DEFAULT_JWT_ALGORITHM,
    DEFAULT_LEEWAY_SECONDS,
    DEFAULT_REFRESH_MAX_AGE_SECONDS,
    SessionPairFactory,
)
from recc.variables.crypto import SIGNATURE_SIZE
from recc.variables.database import CONFIG_PREFIX_RECC_ARGPARSE_CONFIG


class Context(
    ContextConfig,
    ContextGroup,
    ContextInfo,
    ContextPlugin,
    ContextProject,
    ContextRole,
    ContextSystem,
    ContextUser,
):
    """
    Core context.
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        *,
        loop: Optional[AbstractEventLoop] = None,
        skip_assertion=False,
    ):
        self._config = config if config else Config.default()
        self._init_logger()
        self._init_loop(loop)
        self._init_signature()
        self._init_session_factory()
        self._init_cache_store()
        self._init_database()
        self._init_plugin_manager()

        if skip_assertion:
            return

        assert self._config is not None
        assert self._signature is not None
        assert self._session_factory is not None
        assert self._cache is not None
        assert self._database is not None
        assert self._plugins is not None

    def _init_logger(self) -> None:
        init_logger(
            self._config.log_config,
            self._config.log_level,
            self._config.log_simply,
        )

    def _init_loop(
        self,
        loop: Optional[AbstractEventLoop] = None,
        use_default=True,
    ) -> None:
        if loop is None:
            self._loop = get_event_loop_policy().new_event_loop()
        else:
            self._loop = loop
        if use_default:
            set_event_loop(self._loop)

    def _init_signature(self) -> None:
        if self._config.signature:
            self._signature = str(self._config.signature)
        else:
            self._signature = generate_signature(SIGNATURE_SIZE)
        logger.info(f"Signature: {self._signature}")

    def _init_session_factory(self) -> None:
        assert self._signature
        self._session_factory = SessionPairFactory(
            access_issuer=DEFAULT_ISSUER_RECC_ACCESS,
            refresh_issuer=DEFAULT_ISSUER_RECC_REFRESH,
            access_max_age_seconds=DEFAULT_ACCESS_MAX_AGE_SECONDS,
            refresh_max_age_seconds=DEFAULT_REFRESH_MAX_AGE_SECONDS,
            access_secret=self._signature,
            refresh_secret=self._signature,
            access_algorithm=DEFAULT_JWT_ALGORITHM,
            refresh_algorithm=DEFAULT_JWT_ALGORITHM,
            access_leeway_seconds=DEFAULT_LEEWAY_SECONDS,
            refresh_leeway_seconds=DEFAULT_LEEWAY_SECONDS,
        )
        logger.info("Using the default session factory.")

    def _init_cache_store(self) -> None:
        self._cache = Cache(
            self._config.cache_host,
            self._config.cache_port,
            self._config.cache_secret,
            self._config.cache_prefix,
        )
        logger.info("Created cache-store")

    def _init_database(self) -> None:
        self._database = PgDb(
            self._config.database_host,
            self._config.database_port,
            self._config.database_user,
            self._config.database_pw,
            self._config.database_name,
            self._config.database_timeout,
        )
        logger.info("Created database")

    def _init_plugin_manager(self) -> None:
        self._plugins = CorePluginManager(
            prefix=self._config.plugin_prefix,
            context=self,
            denies=self._config.plugin_deny,
            allows=self._config.plugin_allow,
        )
        logger.info("Created plugin-manager")

    @property
    def version(self) -> str:
        from recc import __version__ as version

        return version

    async def get_database_configs(self) -> Dict[str, str]:
        """
        Configurations stored in the database.
        """

        like = CONFIG_PREFIX_RECC_ARGPARSE_CONFIG + "%"
        infos = await self.get_infos_like(like)
        return {c.key: c.value for c in infos if c.key and c.value}

    async def update_core_plugins_permissions(self) -> None:
        permissions = await self.get_permissions()
        permission_names: Set[str] = set(p.slug for p in permissions if p.slug)
        for key in self._plugins.keys():
            plugin = self._plugins.get(key)
            assert plugin is not None
            for permission in plugin.spec.permissions:
                if permission in permission_names:
                    logger.debug(f"Skip `{key}` core-plugin permission: {permission}")
                else:
                    await self.add_permission(permission)
                    logger.info(f"Add `{key}` core-plugin permission: {permission}")

    async def open(self) -> None:
        self.setup_context_config()
        logger.info("Setup context configurations")

        await self._database.open()
        logger.info("Opened database")

        await self._database.create_tables()
        logger.info("Create tables")
        assert self._database.is_open()

        database_configs = await self.get_database_configs()
        await self.restore_configs(database_configs)
        logger.info("Restores the configuration from the database")

        await self._cache.open()
        logger.info("Opened cache-store")

        await self._after_open()
        logger.info("The context has been opened")

    async def _after_open(self) -> None:
        await self.update_core_plugins_permissions()
        await self._plugins.open()
        logger.info("Opened core-plugins")

    async def close(self) -> None:
        logger.info("Closing the context")

        teardown = self._config.teardown

        await self._plugins.close()
        logger.info("Closed plugin-manager")

        if teardown:
            await self._cache.clear()
            logger.info("Clear caches")

        await self._cache.close()
        logger.info("Closed cache-store")

        if teardown:
            await self._database.drop_tables()
            logger.info("Drop tables")

        await self._database.close()
        logger.info("Closed database")
