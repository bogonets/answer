# -*- coding: utf-8 -*-

import os
from typing import Optional, List, Any, Dict
from Crypto.PublicKey import RSA
from recc.session.session import Session
from recc.blueprint.v1.converter import bp_converter
from recc.container.container_manager_interface import ContainerInfo
from recc.core.mixin.context_base import ContextBase
from recc.exception.recc_error import (
    ReccAlreadyError,
    ReccArgumentError,
    ReccNotReadyError,
    ReccStateError,
    ReccNotFoundError,
    ReccTimeoutError,
)
from recc.struct.task import Task
from recc.rule.naming import valid_naming, naming_task
from recc.log.logging import recc_logger as logger
from recc.rpc.rpc_client import (
    try_connection,
    RpcClient,
    create_rpc_client,
)
from recc.variables.rpc import (
    DEFAULT_WAIT_TASK_INTERVAL,
    DEFAULT_WAIT_TASK_TIMEOUT,
    DEFAULT_WAIT_TASK_RETRIES,
    REGISTER_KEY_RSA_SIZE,
)


class ContextTask(ContextBase):
    async def prepare_task_network(self, group_name: str, project_name: str) -> str:
        network = await self.container.create_task_network_if_not_exist(
            group_name, project_name
        )
        return network.key

    async def prepare_global_task_network(self) -> str:
        return await self.prepare_task_network("", "")

    async def connect_global_network(self) -> None:
        if not self.container.is_open():
            raise ReccNotReadyError("The container-manager is not ready.")

        if self.is_host_mode():
            msg = "You can connect to the global network only in guest mode."
            raise ReccStateError(msg)

        assert self.container_key
        network_key = await self.prepare_global_task_network()

        await self.container.connect_network(network_key, self.container_key)
        logger.info("The container and the global network are connected.")

    async def disconnect_global_network(self) -> None:
        if not self.container.is_open():
            raise ReccNotReadyError("The container-manager is not ready.")

        if self.is_host_mode():
            msg = "You can connect to the global network only in guest mode."
            raise ReccStateError(msg)

        assert self.container_key
        network_key = await self.prepare_global_task_network()

        await self.container.disconnect_network(network_key, self.container_key)
        logger.info("The container and the global network are disconnected.")

    async def prepare_project_volume(self, group_name: str, project_name: str) -> str:
        if self.is_host_mode():
            return self.storage.prepare_project_dir(group_name, project_name)

        volume = await self.container.create_task_volume_if_not_exist(
            group_name, project_name
        )
        return volume.key

    async def prepare_substorage_volume(
        self, group_name: str, project_name: str
    ) -> str:
        if self.is_host_mode():
            return self.storage.prepare_substorage_dir(group_name, project_name)

        volume = await self.container.create_task_volume_if_not_exist(
            group_name, project_name
        )
        return volume.key

    async def upsert_task_db(
        self, group_name: str, project_name: str, task_name: str, **kwargs
    ) -> None:
        project_uid = await self.db.get_project_uid_by_fullpath(
            group_name, project_name
        )
        try:
            task_uid = await self.db.get_task_uid_by_name(project_uid, task_name)
            await self.db.update_task_by_uid(task_uid, **kwargs)  # UPDATE
        except ReccNotFoundError:
            await self.db.create_task(project_uid, **kwargs)  # INSERT

    async def create_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
    ) -> str:
        if self.is_host_mode() and not os.path.isdir(self.storage.get_root_directory()):
            raise ReccNotReadyError("In Host mode, the storage path must be specified.")

        if not valid_naming(group_name):
            raise ReccArgumentError(f"Invalid group name: {group_name}")
        if not valid_naming(project_name):
            raise ReccArgumentError(f"Invalid project name: {project_name}")
        if not valid_naming(task_name):
            raise ReccArgumentError(f"Invalid task name: {task_name}")

        if await self.container.exist_task(group_name, project_name, task_name):
            raise ReccAlreadyError("A container already created exists.")

        container_name = naming_task(group_name, project_name, task_name)
        auth_algorithm = f"RSA({REGISTER_KEY_RSA_SIZE})"
        key = RSA.generate(REGISTER_KEY_RSA_SIZE)
        private_key = str(key.export_key(), "utf-8")
        public_key = str(key.publickey().export_key(), "utf-8")
        workspace_volume = await self.prepare_project_volume(group_name, project_name)
        network_name = await self.prepare_global_task_network()

        container = await self.container.create_task(
            group_name=group_name,
            project_name=project_name,
            task_name=task_name,
            rpc_address=None,
            register_key=public_key,
            maximum_restart_count=maximum_restart_count,
            numa_memory_nodes=numa_memory_nodes,
            base_image_name=base_image_name,
            publish_ports=publish_ports,
            container_name=container_name,
            workspace_volume=workspace_volume,
            network_name=network_name,
        )

        rpc_address = self.storage.get_socket_url(group_name, project_name, task_name)

        try:
            await self.upsert_task_db(
                group_name,
                project_name,
                task_name,
                name=task_name,
                description=description,
                extra=extra,
                rpc_address=rpc_address,
                auth_algorithm=auth_algorithm,
                private_key=private_key,
                public_key=public_key,
                maximum_restart_count=maximum_restart_count,
                numa_memory_nodes=numa_memory_nodes,
                base_image_name=base_image_name,
                publish_ports=publish_ports,
            )
        except BaseException as e:
            logger.exception(e)
            await self.container.remove_container(container.key, force=True)
            raise

        return container

    async def wait_connectable_task_state(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
        interval=DEFAULT_WAIT_TASK_INTERVAL,
        timeout=DEFAULT_WAIT_TASK_TIMEOUT,
        retries=DEFAULT_WAIT_TASK_RETRIES,
    ) -> None:
        if interval <= 0:
            raise ReccArgumentError("'interval' must be greater than 0.")
        if timeout <= 0:
            raise ReccArgumentError("'timeout' must be greater than 0.")
        if retries <= 0:
            raise ReccArgumentError("'retries' must be greater than 0.")

        task = await self.db.get_task_by_fullpath(group_name, project_name, task_name)

        for try_count in range(retries):

            def _try_cb(i: int, max_attempts: int) -> None:
                logger.debug(f"Try connection ({i + 1}/{max_attempts}) ...")

            def _retry_cb(i: int, max_attempts: int) -> None:
                logger.debug(f"Retry connection ({i + 1}/{max_attempts}) ...")

            def _success_cb(i: int, max_attempts: int) -> None:
                logger.info(f"Self connection successful !! ({i + 1}/{max_attempts})")

            def _failure_cb(i: int, max_attempts: int) -> None:
                logger.debug(f"Self connection failure. ({i + 1}/{max_attempts})")

            connection_result = await try_connection(
                task.rpc_address,
                try_cb=_try_cb,
                retry_cb=_retry_cb,
                success_cb=_success_cb,
                failure_cb=_failure_cb,
            )

            if not connection_result:
                raise ReccTimeoutError(f"Connection timeout: {task.rpc_address}")

    async def create_task_client(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> RpcClient:
        task = await self.db.get_task_by_fullpath(group_name, project_name, task_name)
        key = self.tm.key(group_name, project_name, task_name)
        if self.tm.exist(key):
            client = self.tm.get(key)
            if client.is_open():
                await client.close()
            self.tm.remove(key)

        client = create_rpc_client(task.rpc_address)
        await client.open()
        self.tm.set(key, client)
        return client

    async def remove_task_client(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> None:
        key = self.tm.key(group_name, project_name, task_name)
        if self.tm.exist(key):
            client = self.tm.get(key)
            if client.is_open():
                await client.close()
            self.tm.remove(key)

    async def get_task_client(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> RpcClient:
        key = self.tm.key(group_name, project_name, task_name)
        return self.tm.get(key)

    async def log_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> str:
        task = await self.container.get_task(group_name, project_name, task_name)
        return await self.container.logs_container(task.key)

    async def remove_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> None:
        for task in await self.container.get_tasks(group_name, project_name, task_name):
            await self.container.remove_container(task.key, force=True)

    async def start_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> None:
        task = await self.container.get_task(group_name, project_name, task_name)
        await self.container.start_container(task.key)

    async def stop_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> None:
        task = await self.container.get_task(group_name, project_name, task_name)
        await self.container.stop_container(task.key)

    async def restart_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> None:
        task = await self.container.get_task(group_name, project_name, task_name)
        await self.container.restart_container(task.key)

    async def get_tasks(
        self, session: Session, group_name: str, project_name: str
    ) -> List[Task]:
        user = await self.db.get_user_by_username(session.audience)
        group = await self.db.get_group_by_name(group_name)
        project = await self.db.get_project_by_name(group.uid, project_name)
        assert user.uid is not None
        assert group.uid is not None
        assert project.uid is not None

        # TODO: test permission

        return await self.db.get_task_by_project_uid(project.uid)

    async def get_task_status(
        self, session: Session, group_name: str, project_name: str
    ) -> List[ContainerInfo]:
        user = await self.db.get_user_by_username(session.audience)
        group = await self.db.get_group_by_name(group_name)
        project = await self.db.get_project_by_name(group.uid, project_name)
        assert user.uid is not None
        assert group.uid is not None
        assert project.uid is not None

        # TODO: test permission

        return await self.container.get_tasks(group_name, project_name)

    async def set_graph_with_extra_v1(
        self,
        session: Session,
        group_name: str,
        project_name: str,
        extra: Any,
    ) -> None:
        user = await self.db.get_user_by_username(session.audience)
        group = await self.db.get_group_by_name(group_name)
        project = await self.db.get_project_by_name(group.uid, project_name)
        assert user.uid is not None
        assert group.uid is not None
        assert project.uid is not None

        if not isinstance(extra, dict):
            raise ReccArgumentError("extra must be of type `dict`.")

        graph = bp_converter(extra)
        if graph is None:
            raise ReccArgumentError("Could not find `graph` in `extra` argument.")

        if graph.tasks is None:
            raise ReccArgumentError("Could not find `tasks` in `extra` argument.")

        # Clear containers.
        for c in await self.container.get_tasks(group_name, project_name):
            await self.container.remove_container(c.key, force=True)
            logger.info(f"Removed container: {c.name}")

        # Clear task data.
        for t in await self.db.get_task_by_project_uid(project.uid):
            await self.db.delete_task_by_uid(t.uid)
            logger.info(f"Removed task from database: {t.name}")

        for task_name, task in graph.tasks.items():
            await self.create_task(group_name, project_name, task_name)
            await self.start_task(group_name, project_name, task_name)
            await self.wait_connectable_task_state(group_name, project_name, task_name)
            client = await self.create_task_client(group_name, project_name, task_name)
            await client.upload_templates(self.storage.compress_templates())
            await client.set_task_blueprint(self.storage.compress_templates())

        await self.db.update_project_extra_by_uid(project.uid, extra)

    async def send_signal_v1(
        self,
        _: Session,
        project_name: str,
        task_name: str,
        signal_name: str,
        lambda_name: str,
        input_queries: List[str],
        output_queries: List[str],
    ) -> Any:
        return ""

    async def get_lambda_property_value(
        self,
        _: Session,
        project_name: str,
        task_name: str,
        lambda_name: str,
        property_name: str,
    ) -> Any:
        return ""

    async def set_lambda_property_value(
        self,
        _: Session,
        project_name: str,
        task_name: str,
        lambda_name: str,
        property_name: str,
        property_value: Any,
    ) -> None:
        pass
