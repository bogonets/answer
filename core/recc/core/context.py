# -*- coding: utf-8 -*-

import os
from asyncio import AbstractEventLoop, get_event_loop_policy, set_event_loop
from copy import deepcopy
from hashlib import sha256
from shutil import move
from typing import Dict, Optional, Set

from recc.argparse.config.core_config import CoreConfig
from recc.argparse.default_config import get_default_core_config
from recc.argparse.injection_values import injection_core_default_values
from recc.cache.cache import Cache
from recc.container.container_manager import create_container_manager
from recc.core.mixin.context_config import ContextConfig
from recc.core.mixin.context_daemon import ContextDaemon
from recc.core.mixin.context_group import ContextGroup
from recc.core.mixin.context_info import ContextInfo
from recc.core.mixin.context_lamda import ContextLamda
from recc.core.mixin.context_plugin import ContextPlugin
from recc.core.mixin.context_port import ContextPort
from recc.core.mixin.context_project import ContextProject
from recc.core.mixin.context_role import ContextRole
from recc.core.mixin.context_storage import ContextStorage
from recc.core.mixin.context_system import ContextSystem
from recc.core.mixin.context_task import ContextTask
from recc.core.mixin.context_user import ContextUser
from recc.crypto.signature import generate_signature
from recc.daemon.daemon_manager import DaemonManager
from recc.database.pg_db import PgDb
from recc.init.default import (
    init_json_driver,
    init_logger,
    init_loop_driver,
    init_xml_driver,
    init_yaml_driver,
)
from recc.logging.logging import recc_core_logger as logger
from recc.package.requirements_utils import RECC_REQUIREMENTS_MAIN
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
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.task.task_connection_pool import create_task_connection_pool
from recc.util.version import parse_semantic_version, version_text, version_tuple
from recc.variables.crypto import SIGNATURE_SIZE
from recc.variables.database import (
    CONFIG_PREFIX_RECC_ARGPARSE_CONFIG,
    PIP_DOMAIN_RECC,
    PIP_HASH_METHOD_SHA256,
    ROLE_SLUG_OWNER,
    ROLE_UID_OWNER,
)
from recc.variables.logging import VERBOSE_LOGGING_LEVEL_1


class Context(
    ContextConfig,
    ContextDaemon,
    ContextGroup,
    ContextInfo,
    ContextLamda,
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
        self._init_json_driver()
        self._init_xml_driver()
        self._init_yaml_driver()
        self._init_loop_driver()
        self._init_loop(loop)
        self._init_signature()
        self._init_local_storage()
        self._init_session_factory()
        self._init_container_manager()
        self._init_cache_store()
        self._init_database()
        self._init_task_manager()
        self._init_plugin_manager()
        self._init_daemons()

        if skip_assertion:
            return

        assert self._config is not None
        assert self._signature is not None
        assert self._local_storage is not None
        assert self._session_factory is not None
        assert self._container is not None
        assert self._container_key is not None
        assert self._cache is not None
        assert self._database is not None
        assert self._tasks is not None
        assert self._plugins is not None

    def _init_logger(self) -> None:
        init_logger(
            self._config.log_config,
            self._config.log_level,
            self._config.log_simply,
        )

    def _init_json_driver(self) -> None:
        init_json_driver(self._config.json_driver)

    def _init_xml_driver(self) -> None:
        init_xml_driver(self._config.xml_driver)

    def _init_yaml_driver(self) -> None:
        init_yaml_driver(self._config.yaml_driver)

    def _init_loop_driver(self) -> None:
        init_loop_driver(self._config.loop_driver)

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
        if self._config.verbose >= VERBOSE_LOGGING_LEVEL_1:
            logger.info(self._local_storage.template_manager.to_details())

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

    def _init_container_manager(self) -> None:
        self._container = create_container_manager(
            self._config.container_type,
            self._config.container_host,
            self._config.container_port,
        )
        logger.info(f"Created container-manager: {self._config.container_type}")

        # GitLab CI Runner:
        # "label=com.gitlab.gitlab-runner.job.id=$CI_JOB_ID"
        # "label=com.gitlab.gitlab-runner.type=build"

        if self._config.container_id:
            self._container_key = self._config.container_id
        else:
            if self._container.inside_container():
                self._container_key = self._container.get_current_container_key()
            else:
                self._container_key = str()
            if self._container_key:
                logger.info(f"Containers operate in guests: {self._container_key}")
            else:
                logger.info("Containers operate on the host.")

    def _init_cache_store(self) -> None:
        self._cache = Cache(
            self._config.cache_type,
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

    def _init_task_manager(self) -> None:
        self._tasks = create_task_connection_pool()
        logger.info("Created task-manager")

    def _init_plugin_manager(self) -> None:
        self._plugins = CorePluginManager(
            prefix=self._config.core_plugin_prefix,
            context=self,
            denies=self._config.core_plugin_deny,
            allows=self._config.core_plugin_allow,
        )
        logger.info("Created plugin-manager")

    def _init_daemons(self) -> None:
        assert self._local_storage
        self._daemons = DaemonManager(
            prefix=self._config.daemon_plugin_prefix,
            working_root_dir=self._local_storage.daemon_work,
            denies=self._config.daemon_plugin_deny,
            allows=self._config.daemon_plugin_allow,
        )
        logger.info("Created daemon-manager")

    @classmethod
    def version_text(cls) -> str:
        return version_text

    @classmethod
    def version_tuple(cls) -> tuple:
        return version_tuple

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
                await self._database.migration(db_version_tuple, version_tuple)
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

    async def download_pip_packages(
        self,
        domain: str,
        hash_method: str,
        logging_encoding="utf-8",
    ) -> None:
        assert self._local_storage
        assert self._database
        assert self._database.is_open()

        def _stdout_callback(data: bytes) -> None:
            line = str(data, encoding=logging_encoding).rstrip()
            if line:
                logger.debug(line)

        def _stderr_callback(data: bytes) -> None:
            line = str(data, encoding=logging_encoding).rstrip()
            if line:
                logger.warning(line)

        for package in RECC_REQUIREMENTS_MAIN:
            if await self._exists_pip_package(domain, package):
                logger.debug(f"Exists pip package '{package}'")
                continue
            else:
                await self._database.delete_pip_by_domain_and_name(domain, package)

            with self._local_storage.create_temporary_directory() as tmpdir:
                logger.debug(f"Run pip download '{package}'")
                code = await AsyncPythonSubprocess.create_system().download(
                    package,
                    tmpdir,
                    _stdout_callback,
                    _stderr_callback,
                )

                if code == 0:
                    logger.debug(f"Subprocess is done: pip download '{package}'")
                else:
                    raise RuntimeError(f"Error({code}) pip download '{package}'")

                for filename in os.listdir(tmpdir):
                    filepath = os.path.abspath(os.path.join(tmpdir, filename))
                    assert os.path.isfile(filepath)
                    hash_value = self._read_hash(filepath, hash_method)

                    dest = os.path.join(self._local_storage.pip_download, filename)
                    if os.path.exists(dest):
                        try:
                            os.remove(dest)
                            logger.debug(f"Remove the existing pip file: '{dest}'")
                        except BaseException as e:
                            logger.warning(f"Error remove existing pip file: {e}")
                            continue

                    try:
                        move(filepath, dest)
                    except BaseException as e:
                        logger.warning(f"Error moving downloaded pip file: {e}")
                        continue

                    try:
                        await self._database.insert_pip(
                            domain, package, filename, hash_method, hash_value
                        )
                    except BaseException as e:
                        logger.warning(f"Database insert error: {e}")
                        continue

                logger.debug(f"Done pip download '{package}'")

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

    async def open_enabled_daemons(self) -> None:
        daemons = await self._database.select_daemons()
        for daemon in daemons:
            if not daemon.enable:
                logger.debug(f"Daemon<{daemon.slug}> Skipped opening")
                continue

            logger.debug(f"Daemon<{daemon.slug}> Opening ...")
            try:
                await self._daemons.run(daemon.slug, daemon.plugin, daemon.address)
            except BaseException as e:
                logger.error(f"Daemon<{daemon.slug}> Open failed: {e}")
            else:
                logger.info(f"Daemon<{daemon.slug}> Opened")

    async def open(self) -> None:
        await self._test_recc_subprocess()

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

        if self._config.skip_pip_download:
            logger.debug("Skip downloading the pip requirements")
        else:
            logger.debug("Download pip requirements ...")
            await self.download_pip_packages(PIP_DOMAIN_RECC, PIP_HASH_METHOD_SHA256)
            logger.info("Complete downloading all pip requirements")

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
                logger.info("Default-task-image successfully created")

        if self.is_guest_mode():
            await self.connect_global_network()
            logger.info("Guest network mode: connect global network")
        else:
            logger.debug("Host network mode")

        await self._cache.open()
        logger.info("Opened cache-store")

        await self._tasks.open()
        logger.info("Opened task-manager")

        await self._after_open()
        logger.info("The context has been opened")

    async def _after_open(self) -> None:
        await self.update_core_plugins_permissions()
        await self._plugins.open()
        logger.info("Opened core-plugins")

        await self.open_enabled_daemons()
        logger.info("Opened daemon-manager")

    async def _before_close(self) -> None:
        await self._daemons.close()
        logger.info("Closed daemon-manager")

        if self.container.is_open() and self.is_guest_mode():
            await self.disconnect_global_network()
            logger.info("Disconnect global network")

    async def close(self) -> None:
        logger.info("Closing the context")
        await self._before_close()

        teardown = self._config.teardown

        await self._plugins.close()
        logger.info("Closed plugin-manager")

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
