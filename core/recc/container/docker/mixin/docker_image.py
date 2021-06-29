# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from io import BytesIO
from docker.models.images import Image
from recc.log.logging import recc_container_logger as logger
from recc.container.docker.mixin.docker_base import DockerBase
from recc.container.container_manager_interface import ImageInfo
from recc.variables.container import (
    BUILD_CONTEXT_BUILD_PATH,
    BUILD_CONTEXT_DOCKERFILE_PATH,
)


def _create_image_info(image: Image) -> ImageInfo:
    key = image.id
    tags = image.tags
    labels = image.labels if image.labels else dict()
    return ImageInfo(key, tags, labels)


class DockerImage(DockerBase):
    async def images(
        self,
        name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        show_all: bool = False,
    ) -> List[ImageInfo]:
        result = list()
        logger.info(f"Listing the image: {name}")
        for image in self.docker.images.list(name, all=show_all, filters=filters):
            result.append(_create_image_info(image))
        return result

    async def build_image(
        self,
        tarfile: bytes,
        name: str,
        path=BUILD_CONTEXT_BUILD_PATH,
        script_path=BUILD_CONTEXT_DOCKERFILE_PATH,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        logger.info(f"Build the image: {name}")
        image_object, build_logs = self.docker.images.build(
            path=path,
            fileobj=BytesIO(tarfile),
            tag=name,
            custom_context=True,
            dockerfile=script_path,
            rm=True,  # Remove intermediate containers
            **kwargs,
        )
        assert image_object
        return list(build_logs)

    async def pull_image(self, image: str, **kwargs) -> None:
        name, tag = image.split(":", 2)
        self.docker.images.pull(name, tag if tag else None, all_tags=False, **kwargs)

    async def remove_image(self, image: str, force=False, no_prune=False) -> None:
        self.docker.images.remove(image, force, no_prune)
