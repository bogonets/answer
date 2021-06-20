# -*- coding: utf-8 -*-

from typing import Optional
from recc.variables.orchestration import (
    CM_TYPE_NAME_DOCKER,
    CM_TYPE_NAME_SWARM,
    CM_TYPE_NAME_KUBERNETES,
)
from recc.container.async_cm_interface import AsyncContainerManagerInterface
from recc.container.docker.async_docker import AsyncDockerContainerManager


def create_container_manager(
    cm_type: str,
    cm_host: Optional[str] = None,
    cm_port: Optional[int] = None,
) -> AsyncContainerManagerInterface:
    if cm_type == CM_TYPE_NAME_DOCKER:
        return AsyncDockerContainerManager(cm_host, cm_port)
    elif cm_type == CM_TYPE_NAME_SWARM:
        raise NotImplementedError("Swarm type is not supported.")
    elif cm_type == CM_TYPE_NAME_KUBERNETES:
        raise NotImplementedError("Kubernetes type is not supported.")
    else:
        raise ValueError(f"Unknown container-manager type: {cm_type}")
