# -*- coding: utf-8 -*-

import os
import re
from typing import Optional, List, Dict, Any
from enum import Enum
from docker import DockerClient
from recc.exception.recc_error import (
    ReccNotFoundError,
    ReccArgumentError,
)
from recc.log.logging import recc_cm_logger as logger
from recc.rule.naming import (
    valid_naming,
    naming_task,
    naming_task_volume,
    naming_task_network,
)
from recc.variables.task_guest import (
    TASK_GUEST_WORKSPACE_DIR,
    TASK_GUEST_CACHE_DIR,
    TASK_GUEST_PACKAGE_DIR,
)
from recc.variables.orchestration import DOCKER_SOCK_LOCAL_BASE_URL
from recc.container.labels import (
    task_create_labels,
    task_find_labels,
)
from recc.container.container_manager_interface import (
    ContainerInfo,
    VolumeInfo,
    NetworkInfo,
    ContainerManagerInterface,
)
from recc.variables.orchestration import (
    NODE_IMAGE_NAME,
    NODE_IMAGE_LATEST_FULLNAME,
    DEFAULT_RESTART_COUNT,
    DEFAULT_TIME_ZONE,
)
from recc.container.docker.node_init import COMPRESS_NODE_INIT_TAR_BYTES
from recc.container.docker.mixin.docker_container import DockerContainer
from recc.container.docker.mixin.docker_image import DockerImage
from recc.container.docker.mixin.docker_network import DockerNetwork
from recc.container.docker.mixin.docker_volume import DockerVolume

SELF_CGROUP_PATH = "/proc/self/cgroup"
DOCKER_CGROUP_REGEX = re.compile(r"\d+:[\w=]+:/docker(-[ce]e)?/(\w+)")
NODE_INIT_BYTES = COMPRESS_NODE_INIT_TAR_BYTES


def _get_current_container_key_from_common_host() -> str:
    value = os.environ.get("HOSTNAME")
    if value is None:
        raise ReccNotFoundError("Not found current container key.")
    return value


def _get_current_container_key_from_ubuntu_host() -> str:
    if not os.path.isfile(SELF_CGROUP_PATH):
        raise ReccNotFoundError("Not found cgroup file.")
    with open(SELF_CGROUP_PATH) as f:
        for line in f:
            result = DOCKER_CGROUP_REGEX.search(line)
            if result is None:
                continue
            groups = result.groups()
            assert len(groups) == 2
            assert isinstance(groups[1], str)
            return groups[1]
    raise ReccNotFoundError("Not found current container key. (by cgroup)")


class BaseHostType(Enum):
    Unknown = 0
    Common = 1
    Ubuntu = 2


def _get_current_container_key(host=BaseHostType.Unknown) -> str:
    if host == BaseHostType.Ubuntu:
        return _get_current_container_key_from_ubuntu_host()
    elif host == BaseHostType.Common:
        return _get_current_container_key_from_common_host()

    # Unknown -> Ubuntu
    assert host == BaseHostType.Unknown
    return _get_current_container_key_from_ubuntu_host()


def _inside_container(host=BaseHostType.Unknown) -> bool:
    try:
        _get_current_container_key(host)
    except ReccNotFoundError:
        return False
    else:
        return True


class DockerContainerManager(
    DockerContainer,
    DockerImage,
    DockerNetwork,
    DockerVolume,
    ContainerManagerInterface,
):
    def __init__(self, host=DOCKER_SOCK_LOCAL_BASE_URL, port: Optional[int] = None):
        self._host = host
        self._port = port
        self._docker = None

    @staticmethod
    def inside_container() -> bool:
        return _inside_container()

    @staticmethod
    def get_current_container_key() -> str:
        return _get_current_container_key()

    def is_open(self) -> bool:
        return self._docker is not None

    async def open(self) -> None:
        self._docker = DockerClient(self.base_url)

    async def close(self) -> None:
        assert self._docker
        self._docker.close()
        self._docker = None

    async def version(self, key: Optional[str] = None) -> str:
        version = self.docker.version()
        if key is None:
            return version["Version"]
        return version[key]

    async def exist_default_task_images(self) -> bool:
        available_images = await self.images(NODE_IMAGE_NAME)
        if available_images is None:
            return False
        return NODE_IMAGE_LATEST_FULLNAME in available_images

    async def pull_default_task_images(self) -> None:
        await self.pull_image(NODE_IMAGE_LATEST_FULLNAME)

    async def get_tasks(
        self,
        group_name: Optional[str] = None,
        project_name: Optional[str] = None,
        task_name: Optional[str] = None,
    ) -> List[ContainerInfo]:
        labels = task_find_labels(group_name, project_name, task_name)
        return await self.containers(filters={"label": labels})

    async def get_task(
        self, group_name: str, project_name: str, task_name: str
    ) -> ContainerInfo:
        nodes = await self.get_tasks(group_name, project_name, task_name)
        if not nodes:
            params = f"group={group_name},project={project_name},task={task_name}"
            raise ReccNotFoundError(f"Not found node: {params}")
        return nodes[0]

    async def exist_task(
        self, group_name: str, project_name: str, task_name: str
    ) -> bool:
        nodes = await self.get_tasks(group_name, project_name, task_name)
        if nodes is None or len(nodes) == 0:
            return False
        assert len(nodes) >= 1
        if len(nodes) >= 2:
            logger.warning(f"Multiple containers have been detected: {nodes}")
        return True

    async def get_task_volumes(
        self,
        group_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> List[VolumeInfo]:
        labels = task_find_labels(group_name, project_name)
        return await self.volumes(filters={"label": labels})

    async def get_task_volume(self, group_name: str, project_name: str) -> VolumeInfo:
        volumes = await self.get_task_volumes(group_name, project_name)
        if not volumes:
            params = f"group={group_name},project={project_name}"
            raise ReccNotFoundError(f"Not found volume: {params}")
        return volumes[0]

    async def exist_task_volume(self, group_name: str, project_name: str) -> bool:
        volumes = await self.get_task_volumes(group_name, project_name)
        if volumes is None or len(volumes) == 0:
            return False
        assert len(volumes) >= 1
        if len(volumes) >= 2:
            logger.warning(f"Multiple volumes have been detected: {volumes}")
        return True

    async def get_task_networks(
        self,
        group_name: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> List[NetworkInfo]:
        labels = task_find_labels(group_name, project_name)
        return await self.networks(filters={"label": labels})

    async def get_task_network(self, group_name: str, project_name: str) -> NetworkInfo:
        networks = await self.get_task_networks(group_name, project_name)
        if not networks:
            params = f"group={group_name},project={project_name}"
            raise ReccNotFoundError(f"Not found network: {params}")
        return networks[0]

    async def exist_task_network(self, group_name: str, project_name: str) -> bool:
        networks = await self.get_task_networks(group_name, project_name)
        if networks is None or len(networks) == 0:
            return False
        assert len(networks) >= 1
        if len(networks) >= 2:
            logger.warning(f"Multiple networks have been detected: {networks}")
        return True

    async def create_task_volume_if_not_exist(
        self, group_name: str, project_name: str
    ) -> VolumeInfo:
        name = naming_task_volume(group_name, project_name)
        volumes = await self.get_task_volumes(group_name, project_name)
        if volumes:
            return volumes[0]
        labels = task_create_labels(group_name, project_name)
        return await self.create_volume(name, labels=labels)

    async def create_task_network_if_not_exist(
        self, group_name: str, project_name: str
    ) -> NetworkInfo:
        name = naming_task_network(group_name, project_name)
        networks = await self.get_task_networks(group_name, project_name)
        if networks:
            return networks[0]
        labels = task_create_labels(group_name, project_name)
        return await self.create_network(name, labels=labels, check_duplicate=True)

    async def create_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
        rpc_bind: str,
        rpc_port: int,
        register_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        container_name: Optional[str] = None,
        workspace_volume: Optional[str] = None,
        network_name: Optional[str] = None,
    ) -> ContainerInfo:
        if not valid_naming(group_name):
            raise ReccArgumentError(f"Invalid group name: {group_name}")
        if not valid_naming(project_name):
            raise ReccArgumentError(f"Invalid project name: {project_name}")
        if not valid_naming(task_name):
            raise ReccArgumentError(f"Invalid task name: {task_name}")

        kwargs = {
            "detach": True,
            "environment": {
                "TZ": DEFAULT_TIME_ZONE,
                "PYTHONPATH": TASK_GUEST_PACKAGE_DIR,
                "RECC_TASK_BIND": rpc_bind,
                "RECC_TASK_PORT": rpc_port,
                "RECC_TASK_REGISTER": register_key if register_key else "",
                "RECC_TASK_WORKSPACE": TASK_GUEST_WORKSPACE_DIR,
            },
            "labels": task_create_labels(group_name, project_name, task_name),
            "network": network_name,
            "entrypoint": ["python", "-m", "recc", "task"],
        }

        if container_name:
            kwargs["name"] = container_name
        else:
            kwargs["name"] = naming_task(group_name, project_name, task_name)

        volumes = dict()
        if workspace_volume:
            volumes[workspace_volume] = {
                "bind": TASK_GUEST_WORKSPACE_DIR,
                "mode": "rw",
            }
        if volumes:
            kwargs["volumes"] = volumes

        if network_name:
            kwargs["network"] = network_name
        if numa_memory_nodes:
            kwargs["cpuset_mems"] = numa_memory_nodes
        if maximum_restart_count is not None:
            count: int
            if maximum_restart_count >= 1:
                count = maximum_restart_count
            else:
                count = DEFAULT_RESTART_COUNT
            kwargs["restart_policy"] = {
                "Name": "on-failure",
                "MaximumRetryCount": count,
            }
        if publish_ports:
            kwargs["ports"] = publish_ports

        image = base_image_name if base_image_name else NODE_IMAGE_LATEST_FULLNAME
        container = await self.create_container(image, None, **kwargs)
        assert container is not None
        assert container.key is not None

        try:
            put_result = await self.put_archive(container.key, "/", NODE_INIT_BYTES)
            if not put_result:
                raise RuntimeError("Failed to upload node-init archive.")
        except BaseException as e:
            logger.exception(e)
            await self.remove_container(container.key, force=True)
            raise

        return container
