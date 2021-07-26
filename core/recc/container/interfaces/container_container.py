# -*- coding: utf-8 -*-

from typing import Optional, List, Union, Dict, Any
from abc import ABCMeta, abstractmethod
from tarfile import TarFile
from signal import SIGKILL
from recc.container.struct.container_info import ContainerInfo


class ContainerContainer(metaclass=ABCMeta):
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
