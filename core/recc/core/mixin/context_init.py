# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from asyncio import get_event_loop_policy, set_event_loop
from typing import Optional
from asyncio import AbstractEventLoop
from recc.core.mixin.context_base import ContextBase
from recc.init.default import (
    init_logger,
    init_json_driver,
    init_xml_driver,
    init_yaml_driver,
    init_loop_driver,
)
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.default_namespace import get_default_core_config
from recc.argparse.injection_values import injection_core_default_values
from recc.container.container_manager import create_container_manager
from recc.cache.cache import Cache
from recc.database.database import create_database
from recc.storage.core_storage import CoreStorage
from recc.task.task_connection_pool import create_task_connection_pool
from recc.resource.port_manager import PortManager
from recc.logging.logging import recc_core_logger as logger
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
from recc.variables.crypto import SIGNATURE_SIZE
from recc.variables.logging import VERBOSE_LOGGING_LEVEL_1


class ContextInit(ContextBase):
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

    @staticmethod
    def _create_signature(size: int) -> str:
        return os.urandom(size).hex()

    def _init_signature(self) -> None:
        if self._config.signature:
            self._signature = str(self._config.signature)
        else:
            self._signature = self._create_signature(SIGNATURE_SIZE)
        logger.info(f"Signature: {self._signature}")

    def _init_storage(self) -> None:
        self._storage = CoreStorage(self._config.local_storage)
        root_dir = self._storage.get_root_directory()
        logger.info(f"Created storage-manager (root={root_dir})")
        if self._config.verbose >= VERBOSE_LOGGING_LEVEL_1:
            logger.info(self._storage.get_template_manager().to_details())

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
        assert self._storage

        plugin_dirs = self._storage.find_plugin_dirs()
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

    def init_all(
        self,
        config: Optional[CoreConfig] = None,
        loop: Optional[AbstractEventLoop] = None,
        skip_assertion=False,
    ) -> None:
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
        self._init_storage()
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
        assert self._storage is not None
        assert self._session_factory is not None
        assert self._container is not None
        assert self._container_key is not None
        assert self._cache is not None
        assert self._database is not None
        assert self._tasks is not None
        assert self._ports is not None
        assert self._plugins is not None
