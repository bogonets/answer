# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from typing import Optional, List, Any, Dict, Union
from signal import SIGKILL
from Crypto.PublicKey import RSA
from recc.aio.connection import try_connection
from recc.blueprint.v1.converter import bp_converter
from recc.container.struct.container_status import ContainerStatus
from recc.container.struct.container_info import ContainerInfo
from recc.container.struct.port_binding_guest import PortBindingGuest
from recc.core.mixin.context_base import ContextBase
from recc.rule.naming_base import valid_naming
from recc.rule.naming_task import naming_task
from recc.logging.logging import recc_core_logger as logger
from recc.rpc.rpc_client import (
    heartbeat,
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

    # ---------
    # Container
    # ---------

    async def get_containers(self) -> List[ContainerInfo]:
        return await self.container.containers()

    async def get_container(self, key: str) -> ContainerInfo:
        return await self.container.get_container(key)

    async def start_container(self, key: str) -> None:
        await self.container.start_container(key)

    async def stop_container(self, key: str) -> None:
        await self.container.stop_container(key)

    async def kill_container(self, key: str, signal: Union[str, int] = SIGKILL) -> None:
        await self.container.kill_container(key, signal)

    async def restart_container(self, key: str) -> None:
        await self.container.restart_container(key)

    async def pause_container(self, key: str) -> None:
        await self.container.pause_container(key)

    async def unpause_container(self, key: str) -> None:
        await self.container.unpause_container(key)

    async def remove_container(self, key: str, force=False) -> None:
        await self.container.remove_container(key, force)

    # -----
    # Tasks
    # -----

    async def get_tasks(self, group: str, project: str) -> List[ContainerInfo]:
        return await self.container.get_tasks(group, project)

    # --------
    # Networks
    # --------

    async def prepare_task_network(self, group: str, project: str) -> str:
        network = await self.container.create_task_network_if_not_exist(group, project)
        return network.key

    async def prepare_global_task_network(self) -> str:
        return await self.prepare_task_network("", "")

    async def connect_global_network(self) -> None:
        if not self.container.is_open():
            raise RuntimeError("The container-manager is not ready")

        if self.is_host_mode():
            msg = "You can connect to the global network only in guest mode"
            raise RuntimeError(msg)

        assert self.container_key
        network_key = await self.prepare_global_task_network()

        await self.container.connect_network(network_key, self.container_key)
        logger.info("The container and the global network are connected.")

    async def disconnect_global_network(self) -> None:
        if not self.container.is_open():
            raise RuntimeError("The container-manager is not ready")

        if self.is_host_mode():
            msg = "You can connect to the global network only in guest mode"
            raise RuntimeError(msg)

        assert self.container_key
        network_key = await self.prepare_global_task_network()

        await self.container.disconnect_network(network_key, self.container_key)
        logger.info("The container and the global network are disconnected.")

    async def prepare_project_volume(self, group: str, project: str) -> str:
        if self.is_host_mode():
            return self.storage.prepare_project_dir(group, project)
        volume = await self.container.create_task_volume_if_not_exist(group, project)
        return volume.key

    async def prepare_substorage_volume(self, group: str, project: str) -> str:
        if self.is_host_mode():
            return self.storage.prepare_substorage_dir(group, project)
        volume = await self.container.create_task_volume_if_not_exist(group, project)
        return volume.key

    async def upsert_task_db(
        self, group: str, project: str, task: str, **kwargs
    ) -> None:
        group_uid = await self.get_group_uid(group)
        project_uid = await self.get_project_uid(group_uid, project)
        try:
            task_uid = await self.database.select_task_uid_by_slug(project_uid, task)
            await self.database.update_task_by_uid(task_uid, **kwargs)  # UPDATE
        except BaseException:  # noqa
            await self.database.insert_task(project_uid, task, **kwargs)  # INSERT

    async def run_task(
        self,
        group: str,
        project: str,
        task: str,
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
            raise RuntimeError("In Host mode, the storage path must be specified")

        if not valid_naming(group):
            raise ValueError(f"Invalid group name: {group}")
        if not valid_naming(project):
            raise ValueError(f"Invalid project name: {project}")
        if not valid_naming(task):
            raise ValueError(f"Invalid task name: {task}")

        if await self.container.exist_task(group, project, task):
            raise RuntimeError("A container already created exists")

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

        container_name = naming_task(group, project, task)
        auth_algorithm = f"RSA({REGISTER_KEY_RSA_SIZE})"
        key = RSA.generate(REGISTER_KEY_RSA_SIZE)
        private_key = str(key.export_key(), "utf-8")
        public_key = str(key.publickey().export_key(), "utf-8")
        workspace_volume = await self.prepare_project_volume(group, project)
        network_name = await self.prepare_global_task_network()

        rpc_address = f"{bind}:{port}"
        rpc_protocol = "tcp"
        rpc_guest_port = f"{port}/{rpc_protocol}"
        expose_port: Optional[int] = None

        if self.is_host_mode():
            if rpc_guest_port in ports:
                raise RuntimeError("`publish_ports` must not contain RPC ports")

            expose_port = self.ports.alloc()
            ports[rpc_guest_port] = expose_port

        try:
            container = await self.container.create_task(
                group=group,
                project=project,
                task=task,
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
                raise RuntimeError(f"Invalid status: {container.status}")

            if self.is_host_mode():
                # [WARNING] When a port is assigned, it must be bound in the guest.
                host_bindings = container.ports[PortBindingGuest(port, rpc_protocol)]
                if not host_bindings:
                    raise RuntimeError("No exposed ports")
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
                group, project, task, access_rpc_address
            )

            await self.upsert_task_db(
                group,
                project,
                task,
                name=task,
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

        params = f"group={group},project={project},task={task}"
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
            raise ValueError("'interval' must be greater than 0")
        if timeout <= 0:
            raise ValueError("'timeout' must be greater than 0")
        if retries <= 0:
            raise ValueError("'retries' must be greater than 0")

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
                lambda: heartbeat(rpc_address),
                try_cb=_try_cb,
                retry_cb=_retry_cb,
                success_cb=_success_cb,
                failure_cb=_failure_cb,
            )

            if not connection_result:
                raise TimeoutError(f"Connection timeout: {rpc_address}")

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

    async def get_container_infos(
        self, group_name: str, project_name: str
    ) -> List[ContainerInfo]:
        return await self.container.get_tasks(group_name, project_name)

    async def set_graph_with_extra_v1(
        self,
        group_name: str,
        project_name: str,
        extra: Any,
    ) -> None:
        group_uid = await self.get_group_uid(group_name)
        project_uid = await self.get_project_uid(group_uid, project_name)

        if not isinstance(extra, dict):
            raise TypeError("extra must be of type `dict`")

        graph = bp_converter(extra)
        if graph is None:
            raise KeyError("Could not find `graph` in `extra` argument")

        if graph.tasks is None:
            raise KeyError("Could not find `tasks` in `extra.graph` argument")

        # Clear containers.
        for c in await self.container.get_tasks(group_name, project_name):
            await self.container.remove_container(c.key, force=True)
            logger.info(f"Removed container: {c.name}")

        # Clear task data.
        for t in await self.database.select_task_by_project_uid(project_uid):
            await self.database.delete_task_by_uid(t.uid)
            logger.info(f"Removed task from database: {t.name}")

        for task_name, task in graph.tasks.items():
            client = await self.run_task(group_name, project_name, task_name)
            await client.upload_templates(self.storage.compress_templates())
            await client.set_task_blueprint(task)

        await self.database.update_project_by_uid(project_uid, extra=extra)
