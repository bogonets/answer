# -*- coding: utf-8 -*-

from typing import Optional
from recc.variables.container import (
    CONTAINER_TYPE_DOCKER,
    CONTAINER_TYPE_SWARM,
    CONTAINER_TYPE_KUBERNETES,
)
from recc.container.interfaces.container_interface import ContainerInterface
from recc.container.docker.docker_container_manager import DockerContainerManager


def create_container_manager(
    cm_type: str,
    cm_host: Optional[str] = None,
    cm_port: Optional[int] = None,
) -> ContainerInterface:
    if cm_type == CONTAINER_TYPE_DOCKER:
        return DockerContainerManager(cm_host, cm_port)
    elif cm_type == CONTAINER_TYPE_SWARM:
        raise NotImplementedError("Swarm type is not supported.")
    elif cm_type == CONTAINER_TYPE_KUBERNETES:
        raise NotImplementedError("Kubernetes type is not supported.")
    else:
        raise ValueError(f"Unknown container-manager type: {cm_type}")
