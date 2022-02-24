# -*- coding: utf-8 -*-

from copy import deepcopy
from asyncio import get_event_loop_policy, set_event_loop
from typing import Optional, Dict
from asyncio import AbstractEventLoop

from recc.argparse.config.core_config import CoreConfig
from recc.crypto.signature import generate_signature
from recc.logging.logging import recc_core_logger as logger
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.argparse.default_namespace import get_default_core_config
from recc.argparse.injection_values import injection_core_default_values
from recc.container.container_manager import create_container_manager
from recc.cache.cache import Cache
from recc.database.database import create_database
from recc.storage.local_storage import LocalStorage
from recc.task.task_connection_pool import create_task_connection_pool
from recc.resource.port_manager import PortManager
from recc.plugin.plugin_manager import PluginManager
from recc.daemon.daemon_manager import DaemonManager
from recc.session.session import (
    DEFAULT_ISSUER_RECC_ACCESS,
    DEFAULT_ISSUER_RECC_REFRESH,
    DEFAULT_ACCESS_MAX_AGE_SECONDS,
    DEFAULT_REFRESH_MAX_AGE_SECONDS,
    DEFAULT_JWT_ALGORITHM,
    DEFAULT_LEEWAY_SECONDS,
    SessionPairFactory,
)
from recc.init.default import (
    init_logger,
    init_json_driver,
    init_xml_driver,
    init_yaml_driver,
    init_loop_driver,
)
from recc.util.version import version_text, version_tuple, parse_version_tuple
from recc.variables.crypto import SIGNATURE_SIZE
from recc.variables.logging import VERBOSE_LOGGING_LEVEL_1
from recc.variables.database import (
    CONFIG_PREFIX_RECC_ARGPARSE_CONFIG,
    ROLE_UID_OWNER,
    ROLE_SLUG_OWNER,
)

from recc.core.mixin.context_config import ContextConfig
from recc.core.mixin.context_daemon import ContextDaemon
from recc.core.mixin.context_group import ContextGroup
from recc.core.mixin.context_info import ContextInfo
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


class Context(
    ContextConfig,
    ContextDaemon,
    ContextGroup,
    ContextInfo,
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
        self._init_port_manager()
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
        assert self._ports is not None
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
        self._database = create_database(
            self._config.database_type,
            self._config.database_host,
            self._config.database_port,
            self._config.database_user,
            self._config.database_pw,
            self._config.database_name,
            self._config.database_timeout,
        )
        logger.info(f"Created database: {self._config.database_type}")

    def _init_task_manager(self) -> None:
        self._tasks = create_task_connection_pool()
        logger.info("Created task-manager.")

    def _init_port_manager(self) -> None:
        min_port = self._config.manage_port_min
        max_port = self._config.manage_port_max
        self._ports = PortManager(min_port, max_port)
        logger.info("Created port-manager.")

    def _init_plugin_manager(self) -> None:
        assert self._local_storage

        plugin_dirs = self._local_storage.find_plugin_dirs()
        plugin_names = list(map(lambda x: x.name, plugin_dirs))

        self._plugins = PluginManager()
        self._plugins.create(self, *plugin_dirs)
        for plugin_name, plugin in self._plugins.items():
            if plugin.exists_routes:
                plugin.update_routes()
        logger.info(f"Created plugin-manager: {plugin_names}")

    def _init_daemons(self) -> None:
        self._daemons = DaemonManager()
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

    async def open_database(self) -> None:
        await self._database.open()
        logger.info("Opened database")

        db_version: Optional[str]
        try:
            db_version = await self._database.select_database_version()
        except:  # noqa
            db_version = None

        if db_version:
            db_version_tuple = parse_version_tuple(db_version)
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

    async def get_database_configs(self) -> Dict[str, str]:
        """
        Configurations stored in the database.
        """

        like = CONFIG_PREFIX_RECC_ARGPARSE_CONFIG + "%"
        infos = await self.get_infos_like(like)
        return {c.key: c.value for c in infos if c.key and c.value}

    async def open(self) -> None:
        await self._test_recc_subprocess()

        self.setup_context_config()
        logger.info("Setup context configurations")

        await self.open_database()
        assert self._database.is_open()

        database_configs = await self.get_database_configs()
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

        await self._daemons.open(self._local_storage.daemon, self.database, self._loop)
        logger.info("Opened daemon-manager")

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
