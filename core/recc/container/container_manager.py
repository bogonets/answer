# -*- coding: utf-8 -*-

from typing import Optional
from recc.variables.orchestration import (
    CM_TYPE_NAME_DOCKER,
    CM_TYPE_NAME_SWARM,
    CM_TYPE_NAME_KUBERNETES,
)
from recc.container.container_manager_interface import ContainerManagerInterface
from recc.container.docker.docker_container_manager import DockerContainerManager


def create_container_manager(
    cm_type: str,
    cm_host: Optional[str] = None,
    cm_port: Optional[int] = None,
) -> ContainerManagerInterface:
    if cm_type == CM_TYPE_NAME_DOCKER:
        return DockerContainerManager(cm_host, cm_port)
    elif cm_type == CM_TYPE_NAME_SWARM:
        raise NotImplementedError("Swarm type is not supported.")
    elif cm_type == CM_TYPE_NAME_KUBERNETES:
        raise NotImplementedError("Kubernetes type is not supported.")
    else:
        raise ValueError(f"Unknown container-manager type: {cm_type}")
