# -*- coding: utf-8 -*-

import os
from asyncio import AbstractEventLoop, get_event_loop_policy, set_event_loop
from copy import deepcopy
from hashlib import sha256
from typing import Dict, Optional, Set

from recc_cache import Cache
from recc_database.database.pg_db import PgDb

from recc.argparse.config.core_config import CoreConfig
from recc.argparse.default_config import get_default_core_config
from recc.argparse.injection_values import injection_core_default_values
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
from recc.storage.local_storage import LocalStorage
from recc.util.version import parse_semantic_version, version_text, version_tuple
from recc.variables.crypto import SIGNATURE_SIZE
from recc.variables.database import (
    CONFIG_PREFIX_RECC_ARGPARSE_CONFIG,
    PIP_HASH_METHOD_SHA256,
    ROLE_SLUG_OWNER,
    ROLE_UID_OWNER,
)


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
        config: Optional[CoreConfig] = None,
        *,
        loop: Optional[AbstractEventLoop] = None,
        skip_assertion=False,
    ):
        cloned_config = deepcopy(config if config else get_default_core_config())
        injection_core_default_values(cloned_config)
        self._config = cloned_config

        self._init_logger()
        self._init_loop(loop)
        self._init_signature()
        self._init_local_storage()
        self._init_session_factory()
        self._init_cache_store()
        self._init_database()
        self._init_plugin_manager()

        if skip_assertion:
            return

        assert self._config is not None
        assert self._signature is not None
        assert self._local_storage is not None
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

    def _init_local_storage(self) -> None:
        self._local_storage = LocalStorage(self._config.local_storage)
        logger.info(f"Created storage-manager (root={self._local_storage.root})")

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
            self._config.cache_pw,
            self._config.cache_prefix,
        )
        logger.info(f"Created cache-store: {self._config.cache_type}")

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
            prefix=self._config.core_plugin_prefix,
            context=self,
            denies=self._config.core_plugin_deny,
            allows=self._config.core_plugin_allow,
        )
        logger.info("Created plugin-manager")

    @classmethod
    def version_text(cls) -> str:
        return version_text

    @classmethod
    def version_tuple(cls) -> tuple:
        return version_tuple

    async def migrate_database(self) -> None:
        db_version: Optional[str]
        try:
            db_version = await self._database.select_database_version()
        except:  # noqa
            db_version = None

        if db_version:
            db_version_tuple = parse_semantic_version(db_version)
            if db_version_tuple > version_tuple:
                prefix = "You cannot migrate to a smaller version"
                suffix = f"db({db_version_tuple}) vs current({version_tuple})"
                message = f"{prefix}: {suffix}"
                logger.error(message)
                raise RuntimeError(message)
            elif db_version_tuple < version_tuple:
                # await self._database.migration(db_version_tuple, version_tuple)
                logger.info("Created database tables")
            else:
                assert db_version_tuple == version_tuple
                pass
        else:
            await self._database.create_tables()
            logger.info("Created database tables")

        owner_uid = await self._database.select_role_uid_by_slug(ROLE_SLUG_OWNER)
        if owner_uid != ROLE_UID_OWNER:
            prefix = f"Owner role ID is not {ROLE_UID_OWNER}"
            suffix = f"It's actually {owner_uid}"
            message = f"{prefix}, {suffix}"
            logger.error(message)
            raise RuntimeError(message)

    @staticmethod
    def _read_hash(path: str, method: str) -> str:
        with open(path, "rb") as f:
            content = f.read()
            if method == PIP_HASH_METHOD_SHA256:
                return sha256(content).hexdigest()
            else:
                raise ValueError(f"Unsupported hash method: '{method}'")

    async def _exists_pip_package(self, domain: str, package: str) -> bool:
        assert self._local_storage
        assert self._database
        assert self._database.is_open()

        pip_infos = await self._database.select_pip_by_domain_and_name(domain, package)
        if not pip_infos:
            return False

        assert len(pip_infos) >= 1
        pip_download_dir = self._local_storage.pip_download

        for pip_info in pip_infos:
            pip_path = os.path.join(pip_download_dir, pip_info.file)
            if not os.path.isfile(pip_path):
                logger.warning(f"File not found: {pip_path}")
                return False

            try:
                hash_value = self._read_hash(pip_path, pip_info.hash_method)
                if hash_value != pip_info.hash_value:
                    logger.warning(f"Hash mismatch: {pip_path}")
                    return False
            except ValueError:
                return False

        return True

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

        await self.migrate_database()
        logger.info("Migrated database")
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
