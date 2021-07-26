# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from abc import ABCMeta, abstractmethod
from recc.container.struct.network_info import NetworkInfo


class ContainerNetwork(metaclass=ABCMeta):
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
