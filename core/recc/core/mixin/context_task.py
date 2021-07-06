# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from typing import Optional, List, Any, Dict
from Crypto.PublicKey import RSA
from recc.session.session import Session
from recc.blueprint.v1.converter import bp_converter
from recc.container.container_manager_interface import (
    ContainerStatus,
    ContainerInfo,
    PortBindingGuest,
)
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
from recc.rule.naming_base import valid_naming
from recc.rule.naming_task import naming_task
from recc.log.logging import recc_core_logger as logger
from recc.rpc.rpc_client import (
    try_connection,
    RpcClient,
    create_rpc_client,
)
from recc.variables.rpc import (
    DEFAULT_RPC_BIND,
    DEFAULT_RPC_PORT,
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
        project_uid = await self.database.get_project_uid_by_fullpath(
            group_name, project_name
        )
        try:
            task_uid = await self.database.get_task_uid_by_name(project_uid, task_name)
            await self.database.update_task_by_uid(task_uid, **kwargs)  # UPDATE
        except ReccNotFoundError:
            await self.database.create_task(project_uid, **kwargs)  # INSERT

    async def run_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
        rpc_bind: Optional[str] = None,
        rpc_port: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        wait_interval=DEFAULT_WAIT_TASK_INTERVAL,
        wait_timeout=DEFAULT_WAIT_TASK_TIMEOUT,
        wait_retries=DEFAULT_WAIT_TASK_RETRIES,
        verbose_level: Optional[int] = None,
    ) -> RpcClient:
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

        if rpc_bind:
            bind = rpc_bind
        else:
            bind = DEFAULT_RPC_BIND

        if rpc_port:
            port = rpc_port
        else:
            port = DEFAULT_RPC_PORT

        if publish_ports:
            ports = deepcopy(publish_ports)
        else:
            ports = dict()

        if verbose_level is not None:
            verbose = verbose_level
        else:
            verbose = self.config.verbose

        container_name = naming_task(group_name, project_name, task_name)
        auth_algorithm = f"RSA({REGISTER_KEY_RSA_SIZE})"
        key = RSA.generate(REGISTER_KEY_RSA_SIZE)
        private_key = str(key.export_key(), "utf-8")
        public_key = str(key.publickey().export_key(), "utf-8")
        workspace_volume = await self.prepare_project_volume(group_name, project_name)
        network_name = await self.prepare_global_task_network()

        rpc_address = f"{bind}:{port}"
        rpc_protocol = "tcp"
        rpc_guest_port = f"{port}/{rpc_protocol}"
        expose_port: Optional[int] = None

        if self.is_host_mode():
            if rpc_guest_port in ports:
                raise ValueError("`publish_ports` must not contain RPC ports.")

            expose_port = self.ports.alloc()
            ports[rpc_guest_port] = expose_port

        try:
            container = await self.container.create_task(
                group_name=group_name,
                project_name=project_name,
                task_name=task_name,
                rpc_address=rpc_address,
                register_key=public_key,
                maximum_restart_count=maximum_restart_count,
                numa_memory_nodes=numa_memory_nodes,
                base_image_name=base_image_name,
                publish_ports=ports,
                container_name=container_name,
                workspace_volume=workspace_volume,
                network_name=network_name,
                verbose_level=verbose,
            )
        except BaseException as e:
            logger.exception(e)

            if expose_port is not None:
                self.ports.free(expose_port)
            raise

        try:
            await self.container.start_container(container.key)

            container = await self.container.get_container(container.key)
            if container.status != ContainerStatus.Running:
                raise LookupError(f"Invalid status: {container.status}")

            if self.is_host_mode():
                # [WARNING] When a port is assigned, it must be bound in the guest.
                host_bindings = container.ports[PortBindingGuest(port, rpc_protocol)]
                if not host_bindings:
                    raise RuntimeError("No exposed ports.")
                host_binding_port = host_bindings[0].port
                access_rpc_address = f"localhost:{host_binding_port}"
            else:
                access_rpc_address = f"{container_name}:{port}"

            await self._wait_connectable_task_state(
                access_rpc_address,
                interval=wait_interval,
                timeout=wait_timeout,
                retries=wait_retries,
            )

            client = await self.create_task_client(
                group_name, project_name, task_name, access_rpc_address
            )

            await self.upsert_task_db(
                group_name,
                project_name,
                task_name,
                name=task_name,
                description=description,
                extra=extra,
                rpc_address=access_rpc_address,
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

            if expose_port is not None:
                self.ports.free(expose_port)

            logs = await self.container.logs_container(container.key)
            assert isinstance(logs, bytes)
            logs_text = str(logs, encoding="utf-8").strip()
            logger.error("[Container Log]\n" + logs_text)

            await self.container.remove_container(container.key, force=True)
            raise

        params = f"group={group_name},project={project_name},task={task_name}"
        logger.info(f"run_task({params}) -> {client}")
        return client

    @staticmethod
    async def _wait_connectable_task_state(
        rpc_address: str,
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

        for try_count in range(retries):

            def _try_cb(i: int, max_attempts: int) -> None:
                logger.debug(f"Try connection ({i + 1}/{max_attempts}) ...")

            def _retry_cb(i: int, max_attempts: int) -> None:
                logger.debug(f"Retry connection ({i + 1}/{max_attempts}) ...")

            def _success_cb(i: int, max_attempts: int) -> None:
                logger.debug(f"Self connection successful !! ({i + 1}/{max_attempts})")

            def _failure_cb(i: int, max_attempts: int) -> None:
                logger.debug(f"Self connection failure. ({i + 1}/{max_attempts})")

            connection_result = await try_connection(
                rpc_address,
                try_cb=_try_cb,
                retry_cb=_retry_cb,
                success_cb=_success_cb,
                failure_cb=_failure_cb,
            )

            if not connection_result:
                raise ReccTimeoutError(f"Connection timeout: {rpc_address}")

    async def create_task_client(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
        rpc_address: str,
    ) -> RpcClient:
        key = self.tasks.make_key(group_name, project_name, task_name)
        if self.tasks.exist(key):
            client = self.tasks.get(key)
            if client.is_open():
                await client.close()
            self.tasks.remove(key)

        client = create_rpc_client(rpc_address)
        await client.open()
        self.tasks.set(key, client)
        return client

    async def remove_task_client(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> None:
        key = self.tasks.make_key(group_name, project_name, task_name)
        if self.tasks.exist(key):
            client = self.tasks.get(key)
            if client.is_open():
                await client.close()
            self.tasks.remove(key)

    async def get_task_client(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
    ) -> RpcClient:
        key = self.tasks.make_key(group_name, project_name, task_name)
        return self.tasks.get(key)

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
        user = await self.database.get_user_by_username(session.audience)
        group = await self.database.get_group_by_name(group_name)
        project = await self.database.get_project_by_name(group.uid, project_name)
        assert user.uid is not None
        assert group.uid is not None
        assert project.uid is not None

        # TODO: test permission

        return await self.database.get_task_by_project_uid(project.uid)

    async def get_task_status(
        self, session: Session, group_name: str, project_name: str
    ) -> List[ContainerInfo]:
        user = await self.database.get_user_by_username(session.audience)
        group = await self.database.get_group_by_name(group_name)
        project = await self.database.get_project_by_name(group.uid, project_name)
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
        user = await self.database.get_user_by_username(session.audience)
        group = await self.database.get_group_by_name(group_name)
        project = await self.database.get_project_by_name(group.uid, project_name)
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
        for t in await self.database.get_task_by_project_uid(project.uid):
            await self.database.delete_task_by_uid(t.uid)
            logger.info(f"Removed task from database: {t.name}")

        for task_name, task in graph.tasks.items():
            client = await self.run_task(group_name, project_name, task_name)
            await client.upload_templates(self.storage.compress_templates())
            await client.set_task_blueprint(task)

        await self.database.update_project_extra_by_uid(project.uid, extra)

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
