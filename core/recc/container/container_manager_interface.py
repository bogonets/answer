# -*- coding: utf-8 -*-

from typing import Optional, List, Union, Dict, Any
from abc import ABCMeta, abstractmethod
from enum import Enum
from tarfile import TarFile
from signal import SIGKILL
from recc.exception.recc_error import ReccArgumentError


class PortBindingGuest:

    __slots__ = ("port", "protocol")

    port: int
    protocol: str

    def __init__(self, port: Union[int, str], protocol: str):
        if isinstance(port, int):
            self.port = port
        else:
            self.port = int(port)
        self.protocol = protocol

    def __str__(self) -> str:
        return f"{self.port}/{self.protocol}"

    def __repr__(self):
        return f"PortBindingGuest<{self.__str__()}>"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)


class PortBindingHost:

    __slots__ = ("ip", "port")

    ip: str
    port: int

    def __init__(self, ip: str, port: Union[int, str]):
        self.ip = ip
        if isinstance(port, int):
            self.port = port
        else:
            self.port = int(port)

    def __str__(self) -> str:
        return f"{self.ip}:{self.port}"

    def __repr__(self):
        return f"PortBindingHost<{self.__str__()}>"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)


class ContainerStatus(Enum):

    Created = 0
    Restarting = 1
    Running = 2
    Removing = 3
    Paused = 4
    Exited = 5
    Dead = 6

    @classmethod
    def from_str(cls, text: str):
        status_key = text[0].upper() + text[1:].lower()
        statuses = [s for s in dir(cls) if not s.startswith("_")]
        if status_key in statuses:
            return getattr(cls, status_key)
        raise KeyError(f"Not found '{status_key}' enum in {cls.__name__}")


class ContainerInfo:

    __slots__ = ("key", "name", "status", "labels", "ports")

    key: str
    name: str
    status: ContainerStatus
    labels: Dict[str, str]
    ports: Dict[PortBindingGuest, List[PortBindingHost]]

    def __init__(
        self,
        key: str,
        name: str,
        status: ContainerStatus,
        labels: Dict[str, str],
        ports: Dict[PortBindingGuest, List[PortBindingHost]],
    ):
        self.key = key
        self.name = name
        if isinstance(status, str):
            self.status = ContainerStatus.from_str(status)
        elif isinstance(status, int):
            self.status = ContainerStatus(status)
        elif isinstance(status, ContainerStatus):
            self.status = status
        else:
            raise ReccArgumentError(f"Unsupported status type: {type(status)}")
        self.labels = labels
        self.ports = ports


class VolumeInfo:

    __slots__ = ("key", "name", "labels")

    key: str
    name: str
    labels: Dict[str, str]

    def __init__(
        self,
        key: str,
        name: str,
        labels: Dict[str, str],
    ):
        self.key = key
        self.name = name
        self.labels = labels


class NetworkInfo:

    __slots__ = ("key", "name", "labels")

    key: str
    name: str
    labels: Dict[str, str]

    def __init__(
        self,
        key: str,
        name: str,
        labels: Dict[str, str],
    ):
        self.key = key
        self.name = name
        self.labels = labels


class ImageInfo:

    __slots__ = ("key", "tags", "labels")

    key: str
    tags: List[str]
    labels: Dict[str, str]

    def __init__(
        self,
        key: str,
        tags: List[str],
        labels: Dict[str, str],
    ):
        self.key = key
        self.tags = tags
        self.labels = labels


class ContainerManagerInterface(metaclass=ABCMeta):
    """
    Container Manager (OS-level virtualization) interface.
    """

    @staticmethod
    @abstractmethod
    def inside_container() -> bool:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_current_container_key() -> str:
        raise NotImplementedError

    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def version(self, key: Optional[str] = None) -> str:
        raise NotImplementedError

    # -----
    # Image
    # -----

    @abstractmethod
    async def images(
        self,
        name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        show_all: bool = False,
    ) -> List[ImageInfo]:
        raise NotImplementedError

    @abstractmethod
    async def build_image(
        self,
        tarfile: bytes,
        name: str,
        path: str,
        script_path: str,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def pull_image(self, image: str, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_image(self, image: str, force=False, no_prune=True) -> None:
        raise NotImplementedError

    # ------
    # Volume
    # ------

    @abstractmethod
    async def volumes(
        self, filters: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[VolumeInfo]:
        raise NotImplementedError

    @abstractmethod
    async def exist_volume(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_volume(self, name: str, **kwargs) -> VolumeInfo:
        raise NotImplementedError

    @abstractmethod
    async def remove_volume(self, key: str, force=False) -> None:
        raise NotImplementedError

    # -------
    # Network
    # -------

    @abstractmethod
    async def networks(
        self, filters: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[NetworkInfo]:
        raise NotImplementedError

    @abstractmethod
    async def exist_network(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_network(self, name: str, **kwargs) -> NetworkInfo:
        raise NotImplementedError

    @abstractmethod
    async def remove_network(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def connect_network(self, key: str, container_key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def disconnect_network(
        self, key: str, container_key: str, force=False
    ) -> None:
        raise NotImplementedError

    # ---------
    # Container
    # ---------

    @abstractmethod
    async def containers(
        self,
        filters: Optional[Dict[str, Any]] = None,
        show_all: bool = False,
        **kwargs,
    ) -> List[ContainerInfo]:
        raise NotImplementedError

    @abstractmethod
    async def get_container(self, key: str) -> ContainerInfo:
        raise NotImplementedError

    @abstractmethod
    async def create_container(
        self, image: str, command: Optional[Union[str, List[str]]] = None, **kwargs
    ) -> ContainerInfo:
        raise NotImplementedError

    @abstractmethod
    async def exist_container(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def remove_container(self, key: str, force=False) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_container(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop_container(self, key: str, timeout: Optional[int] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def restart_container(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def pause_container(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def unpause_container(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def kill_container(self, key: str, signal: Union[str, int] = SIGKILL) -> None:
        raise NotImplementedError

    @abstractmethod
    async def interrupt_container(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def wait_container(self, key: str, timeout: Optional[float] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def logs_container(self, key: str, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_archive(self, key: str, path: str) -> TarFile:
        raise NotImplementedError

    @abstractmethod
    async def put_archive(self, key: str, path: str, data: bytes) -> bool:
        raise NotImplementedError

    # ----
    # Node
    # ----

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
