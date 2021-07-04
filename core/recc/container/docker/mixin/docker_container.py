# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any, Union
from tarfile import open as tar_open
from tarfile import TarFile
from signal import SIGINT, SIGKILL
from io import BytesIO
from docker.models.containers import Container
from recc.container.container_manager_interface import (
    ContainerInfo,
    PortBindingGuest,
    PortBindingHost,
)
from recc.container.docker.mixin.docker_base import DockerBase


def _create_container_ports(
    ports: Dict[str, List[Dict[str, str]]],
) -> Dict[PortBindingGuest, List[PortBindingHost]]:
    result = dict()
    for key, val in ports.items():
        guest_port, guest_protocol = key.split("/", 1)
        guest = PortBindingGuest(guest_port, guest_protocol)
        port_binding_host = list()
        assert isinstance(val, list)
        for host_infos in val:
            assert isinstance(host_infos, dict)
            host_ip = host_infos.get("HostIp")
            if not host_ip:
                continue
            host_port = host_infos.get("HostPort")
            if not host_port:
                continue
            port_binding_host.append(PortBindingHost(host_ip, host_port))
        result[guest] = port_binding_host
    return result


def _create_container_info(container: Container) -> ContainerInfo:
    # Reference: https://docs.docker.com/engine/api/v1.41/#operation/ContainerInspect
    key = container.id
    name = container.name
    state = container.attrs["State"]["Status"]
    if container.labels:
        labels = container.labels
    else:
        labels = dict()
    if container.ports:
        ports = _create_container_ports(container.ports)
    else:
        ports = dict()
    # created = container.attrs["Created"]
    # path = container.attrs["Path"]
    # args = container.attrs["Args"]
    # state = container.attrs["State"]
    # image = container.attrs["Image"]
    # resolv_conf_path = container.attrs["ResolvConfPath"]
    # hostname_path = container.attrs["HostnamePath"]
    # hosts_path = container.attrs["HostsPath"]
    # log_path = container.attrs["LogPath"]
    # restart_count = container.attrs["RestartCount"]
    # driver = container.attrs["Driver"]
    # platform = container.attrs["Platform"]
    # mount_label = container.attrs["MountLabel"]
    # process_label = container.attrs["ProcessLabel"]
    # app_armor_profile = container.attrs["AppArmorProfile"]
    # exec_ids = container.attrs["ExecIDs"]
    # host_config = container.attrs["HostConfig"]
    # graph_driver = container.attrs["GraphDriver"]
    # mounts = container.attrs["Mounts"]
    # config = container.attrs["Config"]
    # network_settings = container.attrs["NetworkSettings"]
    assert key is not None
    assert name is not None
    assert state is not None
    assert labels is not None
    assert ports is not None
    return ContainerInfo(key, name, state, labels, ports)


class DockerContainer(DockerBase):
    async def containers(
        self,
        filters: Optional[Dict[str, Any]] = None,
        show_all: bool = True,
        **kwargs,
    ) -> List[ContainerInfo]:
        container_objects = self.docker.containers.list(
            all=show_all, filters=filters, **kwargs
        )
        return [_create_container_info(c) for c in container_objects]

    async def get_container(self, key: str) -> ContainerInfo:
        for c in await self.containers(show_all=True):
            if c.key == key:
                return c
        raise KeyError(f"Not found container: {key}")

    async def create_container(
        self, image: str, command: Optional[Union[str, List[str]]] = None, **kwargs
    ) -> ContainerInfo:
        container = self.docker.containers.create(image, command, **kwargs)
        return _create_container_info(container)

    def _get_container(self, key: str) -> Container:
        return self.docker.containers.get(key)

    async def exist_container(self, key: str) -> bool:
        try:
            return self._get_container(key) is not None
        except:  # noqa
            return False

    async def remove_container(self, key: str, force=False) -> None:
        self._get_container(key).remove(force=force)

    async def start_container(self, key: str) -> None:
        self._get_container(key).start()

    async def stop_container(self, key: str, timeout: Optional[int] = None) -> None:
        kwargs = dict()
        if timeout is not None:
            kwargs["timeout"] = int(timeout)
        self._get_container(key).stop(**kwargs)

    async def restart_container(self, key: str) -> None:
        self._get_container(key).restart()

    async def pause_container(self, key: str) -> None:
        self._get_container(key).pause()

    async def unpause_container(self, key: str) -> None:
        self._get_container(key).unpause()

    async def kill_container(self, key: str, signal: Union[str, int] = SIGKILL) -> None:
        self._get_container(key).kill(signal)

    async def interrupt_container(self, key: str) -> None:
        await self.kill_container(key, signal=SIGINT)

    async def wait_container(self, key: str, timeout: Optional[float] = None) -> None:
        kwargs = dict()
        if timeout is not None:
            kwargs["timeout"] = int(timeout)
        self._get_container(key).wait(**kwargs)

    async def logs_container(self, key: str, **kwargs) -> Any:
        return self._get_container(key).logs(**kwargs)

    async def get_archive(self, key: str, path: str) -> TarFile:
        bits, stat = self._get_container(key).get_archive(path)
        return tar_open(mode="r", fileobj=BytesIO(bits))

    async def put_archive(self, key: str, path: str, data: bytes) -> bool:
        return self._get_container(key).put_archive(path, data)
