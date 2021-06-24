# -*- coding: utf-8 -*-

import os
from asyncio import get_event_loop_policy, set_event_loop
from typing import Optional
from asyncio import AbstractEventLoop
from recc.core.mixin.context_base import ContextBase
from recc.init.default import init_logger, init_json_driver, init_loop_driver
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.default_namespace import get_default_core_config
from recc.container.container_manager import create_container_manager
from recc.cache.async_cs import create_cache_store
from recc.database.async_db import create_database
from recc.storage.async_sm import AsyncStorageManager
from recc.rpc.async_rpc_client_manager import create_rpc_client_manager
from recc.log.logging import recc_logger as logger
from recc.session.session import (
    DEFAULT_ISSUER_RECC_ACCESS,
    DEFAULT_ISSUER_RECC_REFRESH,
    DEFAULT_ACCESS_MAX_AGE_SECONDS,
    DEFAULT_REFRESH_MAX_AGE_SECONDS,
    DEFAULT_JWT_ALGORITHM,
    DEFAULT_LEEWAY_SECONDS,
    SessionPairFactory,
)

SIGNATURE_SIZE = 32


class ContextInit(ContextBase):
    def _init_logger(self) -> None:
        init_logger(self._config.log_config, self._config.log_level)

    def _init_json_driver(self) -> None:
        init_json_driver(self._config.json_driver)

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
        self._sm = AsyncStorageManager(self._config.storage_root)
        logger.info(f"Created storage-manager (root={self._sm.root})")

    def _init_session_factory(self) -> None:
        assert self._signature
        self._sf = SessionPairFactory(
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
        self._cm = create_container_manager(
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
            if self._cm.inside_container():
                self._container_key = self._cm.get_current_container_key()
            else:
                self._container_key = str()
            if self._container_key:
                logger.info(f"Containers operate in guests: {self._container_key}")
            else:
                logger.info("Containers operate on the host.")

    def _init_cache_store(self) -> None:
        self._cs = create_cache_store(
            self._config.cache_type,
            self._config.cache_host,
            self._config.cache_port,
            self._config.cache_pw,
        )
        logger.info(f"Created cache-store: {self._config.cache_type}")

    def _init_database(self) -> None:
        self._db = create_database(
            self._config.database_type,
            self._config.database_host,
            self._config.database_port,
            self._config.database_user,
            self._config.database_pw,
            self._config.database_name,
        )
        logger.info(f"Created database: {self._config.database_type}")

    def _init_task_manager(self) -> None:
        self._tm = create_rpc_client_manager()
        logger.info("Created task-manager.")

    def init_all(
        self,
        config: Optional[CoreConfig] = None,
        loop: Optional[AbstractEventLoop] = None,
        skip_assertion: Optional[bool] = None,
    ) -> None:
        self._config = config if config else get_default_core_config()
        self._init_logger()
        self._init_json_driver()
        self._init_loop_driver()
        self._init_loop(loop)
        self._init_signature()
        self._init_storage()
        self._init_session_factory()
        self._init_container_manager()
        self._init_cache_store()
        self._init_database()
        self._init_task_manager()

        if skip_assertion:
            return

        assert self._config
        assert self._signature
        assert self._sm
        assert self._sf
        assert self._cm
        assert self._cs
        assert self._db
