# -*- coding: utf-8 -*-

import os
import re
from typing import Optional, List, Dict, Any
from enum import Enum
from docker import DockerClient
from recc.exception.recc_error import (
    ReccNotFoundError,
    ReccArgumentError,
    ReccAlreadyError,
)
from recc.log.logging import recc_cm_logger as logger
from recc.rule.naming import (
    valid_naming,
    naming_task,
    naming_task_volume,
    naming_task_network,
)
from recc.variables.container import DOCKER_SOCK_LOCAL_BASE_URL
from recc.container.labels import (
    task_create_labels,
    task_find_labels,
    task_image_find_labels,
)
from recc.container.container_manager_interface import (
    ContainerInfo,
    VolumeInfo,
    NetworkInfo,
    ImageInfo,
    ContainerManagerInterface,
)
from recc.container.docker.task_init import (
    BUILD_CONTEXT_BUILD_PATH,
    BUILD_CONTEXT_DOCKERFILE_PATH,
    RECC_MODULE_TAR_BYTES_SHA256,
    TASK_GUEST_WORKSPACE_DIR,
    TASK_GUEST_STORAGE_DIR,
    TASK_GUEST_CACHE_DIR,
    get_compressed_task_dockerfile_tar,
)
from recc.variables.container import (
    NODE_IMAGE_LATEST_FULLNAME,
    DEFAULT_RESTART_COUNT,
    DEFAULT_TIME_ZONE,
)
from recc.variables.labels import (
    RECC_IMAGE_VERSION_KEY,
    RECC_IMAGE_SHA256_KEY,
)

from recc.util.version import version_text
from recc.container.docker.mixin.docker_container import DockerContainer
from recc.container.docker.mixin.docker_image import DockerImage
from recc.container.docker.mixin.docker_network import DockerNetwork
from recc.container.docker.mixin.docker_volume import DockerVolume

SELF_CGROUP_PATH = "/proc/self/cgroup"
DOCKER_CGROUP_REGEX = re.compile(r"\d+:[\w=]+:/docker(-[ce]e)?/(\w+)")


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

    async def exist_default_task_images(self, validate_labels=True) -> bool:
        available_images = await self.get_task_images()
        if available_images is None:
            return False

        found_image = None
        for image in available_images:
            if NODE_IMAGE_LATEST_FULLNAME in image.tags:
                found_image = image
                break

        if found_image is None:
            return False
        if not validate_labels:
            return True

        labels = found_image.labels
        if version_text != labels.get(RECC_IMAGE_VERSION_KEY):
            return False
        if RECC_MODULE_TAR_BYTES_SHA256 != labels.get(RECC_IMAGE_SHA256_KEY):
            return False
        return True

    async def create_default_task_images(
        self, remove_previous=True, force=False
    ) -> None:
        if remove_previous:
            images = await self.get_task_images()
            if images:
                for image in images:
                    await self.remove_image(image.key, force)
        await self.create_task_image()

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

    async def get_task_images(self) -> List[ImageInfo]:
        labels = task_image_find_labels()
        return await self.images(filters={"label": labels})

    async def create_task_image(
        self,
        image_full_name: Optional[str] = None,
        base_image: Optional[str] = None,
        recc_version: Optional[str] = None,
        group_name: Optional[str] = None,
        user_name: Optional[str] = None,
        extra_root_commands: Optional[str] = None,
        extra_user_commands: Optional[str] = None,
    ) -> None:
        image_name = image_full_name if image_full_name else NODE_IMAGE_LATEST_FULLNAME
        if image_name in await self.images():
            raise ReccAlreadyError(f"Docker image already exists: {image_name}")

        context_bytes = get_compressed_task_dockerfile_tar(
            base_image=base_image,
            recc_version=recc_version,
            group_name=group_name,
            user_name=user_name,
            extra_root_commands=extra_root_commands,
            extra_user_commands=extra_user_commands,
        )

        try:
            logger.info(f"Building docker image: {image_name} ...")
            build_log = await self.build_image(
                context_bytes,
                image_name,
                BUILD_CONTEXT_BUILD_PATH,
                BUILD_CONTEXT_DOCKERFILE_PATH,
            )
            if build_log:
                logger.info(f"Build message: {build_log}")
            else:
                logger.info("Empty build message")
        finally:
            if image_name in await self.images():
                await self.remove_image(image_name)

    async def create_task(
        self,
        group_name: str,
        project_name: str,
        task_name: str,
        rpc_bind: Optional[str] = None,
        rpc_port: Optional[int] = None,
        register_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        container_name: Optional[str] = None,
        workspace_volume: Optional[str] = None,
        task_storage_volume: Optional[str] = None,
        network_name: Optional[str] = None,
        verbose_level=0,
    ) -> ContainerInfo:
        if not valid_naming(group_name):
            raise ReccArgumentError(f"Invalid group name: {group_name}")
        if not valid_naming(project_name):
            raise ReccArgumentError(f"Invalid project name: {project_name}")
        if not valid_naming(task_name):
            raise ReccArgumentError(f"Invalid task name: {task_name}")

        kwargs = {
            "detach": True,
            "labels": task_create_labels(group_name, project_name, task_name),
            "network": network_name,
            "tmpfs": {TASK_GUEST_CACHE_DIR: ""},
        }

        environment = {
            "TZ": DEFAULT_TIME_ZONE,
            "RECC_TASK_GROUP": group_name,
            "RECC_TASK_PROJECT": project_name,
            "RECC_TASK_TASK": task_name,
        }
        if rpc_bind:
            environment["RECC_TASK_BIND"] = rpc_bind
        if rpc_port:
            environment["RECC_TASK_PORT"] = str(rpc_port)
        if register_key:
            environment["RECC_TASK_REGISTER"] = register_key
        if verbose_level:
            environment["RECC_VERBOSE"] = str(verbose_level)
        kwargs["environment"] = environment

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
        if task_storage_volume:
            volumes[task_storage_volume] = {
                "bind": TASK_GUEST_STORAGE_DIR,
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
        container = await self.create_container(image, ["task"], **kwargs)
        assert container is not None
        assert container.key is not None
        return container
