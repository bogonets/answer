# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from abc import ABCMeta, abstractmethod
from recc.container.struct.image_info import ImageInfo


class ContainerImage(metaclass=ABCMeta):
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
