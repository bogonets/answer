# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional

from recc.container.struct.volume_info import VolumeInfo


class ContainerVolume(metaclass=ABCMeta):
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
