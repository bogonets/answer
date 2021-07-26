# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from abc import ABCMeta, abstractmethod
from recc.container.struct.container_info import ContainerInfo
from recc.container.struct.volume_info import VolumeInfo
from recc.container.struct.network_info import NetworkInfo
from recc.container.struct.image_info import ImageInfo


class ContainerTask(metaclass=ABCMeta):
    @abstractmethod
    async def exist_default_task_images(self, validate_labels=True) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_default_task_images(
        self, remove_previous=True, force=False
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_tasks(
        self,
        group_name: Optional[str] = None,
        project_name: Optional[str] = None,
        task_name: Optional[str] = None,
    ) -> List[ContainerInfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_task(
        self, group_name: str, project_name: str, task_name: str
    ) -> ContainerInfo:
        raise NotImplementedError

    @abstractmethod
    async def exist_task(
        self, group_name: str, project_name: str, task_name: str
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_task_volumes(
        self,
        group_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> List[VolumeInfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_task_volume(self, group_name: str, project_name: str) -> VolumeInfo:
        raise NotImplementedError

    @abstractmethod
    async def exist_task_volume(self, group_name: str, project_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_task_networks(
        self,
        group_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> List[NetworkInfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_task_network(self, group_name: str, project_name: str) -> NetworkInfo:
        raise NotImplementedError

    @abstractmethod
    async def exist_task_network(self, group_name: str, project_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_task_volume_if_not_exist(
        self, group_name: str, project_name: str
    ) -> VolumeInfo:
        raise NotImplementedError

    @abstractmethod
    async def create_task_network_if_not_exist(
        self, group_name: str, project_name: str
    ) -> NetworkInfo:
        raise NotImplementedError

    @abstractmethod
    async def get_task_images(self) -> List[ImageInfo]:
        raise NotImplementedError

    @abstractmethod
    async def create_task_image(
        self,
        image_full_name: Optional[str] = None,
        base_image: Optional[str] = None,
        recc_version: Optional[str] = None,
        group_name: Optional[str] = None,
        user_name: Optional[str] = None,
        extra_commands: Optional[str] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
        rpc_address: Optional[str] = None,
        register_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        container_name: Optional[str] = None,
        workspace_volume: Optional[str] = None,
        network_name: Optional[str] = None,
        verbose_level=0,
    ) -> ContainerInfo:
        """Create a new task.

        :param group_name:
            Group name.
        :param project_name:
            Project name.
        :param task_name:
            Task name.
        :param rpc_address:
            RPC bind address.
        :param register_key:
            Register key. (RSA Public)
        :param maximum_restart_count:
            Maximum number of times to restart the container on failure.
        :param numa_memory_nodes:
            Memory nodes (MEMs) in which to allow execution (0-3, 0,1).
            Only effective on NUMA systems.
        :param base_image_name:
            Base docker image name.
        :param publish_ports:
            Ports to bind inside the container.
            e.g. {"20002/tcp": 8080}, {"20002/tcp", ("127.0.0.1", 8080)}
        :param container_name:
            The container name is determined manually.
        :param workspace_volume:
            Volume name of workspace directory.
        :param network_name:
            Network name.
        :param verbose_level:
            Verbose level.
        """
        raise NotImplementedError
