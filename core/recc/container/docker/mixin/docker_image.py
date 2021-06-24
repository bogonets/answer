# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from io import BytesIO
from recc.log.logging import recc_cm_logger as logger
from recc.container.docker.mixin.docker_base import DockerBase


class DockerImage(DockerBase):
    async def images(
        self,
        name: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        show_all: bool = False,
    ) -> List[str]:
        result = list()
        logger.info(f"Listing the image: {name}")
        for image in self.docker.images.list(name, all=show_all, filters=filters):
            for tag in image.tags:
                result.append(str(tag))
        return result

    async def build_image(
        self,
        tarfile: bytes,
        name: str,
        path: str,
        script_path: str,
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
