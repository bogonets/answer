# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from io import BytesIO, StringIO
from overrides import overrides
from docker.models.images import Image
from recc.logging.logging import recc_container_logger as logger
from recc.container.interfaces.container_image import ContainerImage
from recc.container.docker.mixin.docker_base import DockerBase
from recc.container.struct.image_info import ImageInfo
from recc.variables.container import (
    BUILD_CONTEXT_BUILD_PATH,
    BUILD_CONTEXT_DOCKERFILE_PATH,
)


def _create_image_info(image: Image) -> ImageInfo:
    key = image.id
    tags = image.tags
    labels = image.labels if image.labels else dict()
    return ImageInfo(key, tags, labels)


class DockerImage(ContainerImage, DockerBase):
    @overrides
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

    @overrides
    async def build_image(
        self,
        tarfile: bytes,
        name: str,
        path=BUILD_CONTEXT_BUILD_PATH,
        script_path=BUILD_CONTEXT_DOCKERFILE_PATH,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        logger.info(f"Building `{name}` docker image ...")
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
        result = list(build_logs) if build_logs else list()
        if result:
            stream_buffer = StringIO()
            for stream in result:
                if "stream" in stream:
                    stream_buffer.write(stream["stream"])
                else:
                    stream_buffer.write(str(stream))
            build_message = stream_buffer.getvalue()
            if build_message:
                logger.debug("[BUILD LOG]\n" + build_message)
            else:
                logger.debug("[EMPTY BUILD LOG]")
        return result

    @overrides
    async def pull_image(self, image: str, **kwargs) -> None:
        name, tag = image.split(":", 2)
        self.docker.images.pull(name, tag if tag else None, all_tags=False, **kwargs)

    @overrides
    async def remove_image(self, image: str, force=False, no_prune=False) -> None:
        self.docker.images.remove(image, force, no_prune)
