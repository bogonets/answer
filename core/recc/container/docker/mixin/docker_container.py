# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any, Union
from tarfile import open as tar_open
from tarfile import TarFile
from signal import SIGINT, SIGKILL
from io import BytesIO
from overrides import overrides
from docker.models.containers import Container
from recc.container.interfaces.container_container import ContainerContainer
from recc.container.struct.container_info import ContainerInfo
from recc.container.struct.port_binding_guest import PortBindingGuest
from recc.container.struct.port_binding_host import PortBindingHost
from recc.container.docker.mixin.docker_base import DockerBase

_ERR_FMT_HOST_PORT_TYPE = "The host port information is not a `list` type: %s"


def _create_container_ports(
    ports: Dict[str, List[Dict[str, str]]],
) -> Dict[PortBindingGuest, List[PortBindingHost]]:
    result = dict()
    for key, val in ports.items():
        guest_port, guest_protocol = key.split("/", 1)
        guest = PortBindingGuest(guest_port, guest_protocol)

        port_binding_host = list()
        if val:
            assert isinstance(val, list), _ERR_FMT_HOST_PORT_TYPE % {type(val).__name__}
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
    if container.labels:
        labels = container.labels
    else:
        labels = dict()
    if container.ports:
        ports = _create_container_ports(container.ports)
    else:
        ports = dict()
    created = container.attrs["Created"]
    # path = container.attrs["Path"]
    # args = container.attrs["Args"]
    state = container.attrs["State"]
    status = state["Status"]
    image = container.attrs["Image"]
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
    assert created is not None
    assert status is not None
    assert labels is not None
    assert ports is not None
    return ContainerInfo(
        key=key,
        name=name,
        status=status,
        image=image,
        created=created,
        labels=labels,
        ports=ports,
    )


class DockerContainer(ContainerContainer, DockerBase):
    @overrides
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

    @overrides
    async def get_container(self, key: str) -> ContainerInfo:
        for c in await self.containers(show_all=True):
            if c.key == key:
                return c
        raise KeyError(f"Not found container: {key}")

    @overrides
    async def create_container(
        self, image: str, command: Optional[Union[str, List[str]]] = None, **kwargs
    ) -> ContainerInfo:
        container = self.docker.containers.create(image, command, **kwargs)
        return _create_container_info(container)

    def _get_container(self, key: str) -> Container:
        return self.docker.containers.get(key)

    @overrides
    async def exist_container(self, key: str) -> bool:
        try:
            return self._get_container(key) is not None
        except:  # noqa
            return False

    @overrides
    async def remove_container(self, key: str, force=False) -> None:
        self._get_container(key).remove(force=force)

    @overrides
    async def start_container(self, key: str) -> None:
        self._get_container(key).start()

    @overrides
    async def stop_container(self, key: str, timeout: Optional[int] = None) -> None:
        kwargs = dict()
        if timeout is not None:
            kwargs["timeout"] = int(timeout)
        self._get_container(key).stop(**kwargs)

    @overrides
    async def restart_container(self, key: str) -> None:
        self._get_container(key).restart()

    @overrides
    async def pause_container(self, key: str) -> None:
        self._get_container(key).pause()

    @overrides
    async def unpause_container(self, key: str) -> None:
        self._get_container(key).unpause()

    @overrides
    async def kill_container(self, key: str, signal: Union[str, int] = SIGKILL) -> None:
        self._get_container(key).kill(signal)

    @overrides
    async def interrupt_container(self, key: str) -> None:
        await self.kill_container(key, signal=SIGINT)

    @overrides
    async def wait_container(self, key: str, timeout: Optional[float] = None) -> None:
        kwargs = dict()
        if timeout is not None:
            kwargs["timeout"] = int(timeout)
        self._get_container(key).wait(**kwargs)

    @overrides
    async def logs_container(self, key: str, **kwargs) -> Any:
        return self._get_container(key).logs(**kwargs)

    @overrides
    async def get_archive(self, key: str, path: str) -> TarFile:
        bits, stat = self._get_container(key).get_archive(path)
        return tar_open(mode="r", fileobj=BytesIO(bits))

    @overrides
    async def put_archive(self, key: str, path: str, data: bytes) -> bool:
        return self._get_container(key).put_archive(path, data)
