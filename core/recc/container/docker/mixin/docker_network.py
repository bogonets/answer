# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from docker.models.networks import Network
from recc.container.container_manager_interface import NetworkInfo
from recc.container.docker.mixin.docker_base import DockerBase


def _create_network_info(network: Network) -> NetworkInfo:
    key = network.id
    name = network.name
    labels = network.attrs["Labels"]
    if labels is None:
        labels = dict()
    # created = network.attrs["Created"]
    # scope = network.attrs["Scope"]
    # driver = network.attrs["Driver"]
    # enable_ipv6 = network.attrs["EnableIPv6"]
    # ipam = network.attrs["IPAM"]
    # internal = network.attrs["Internal"]
    # attachable = network.attrs["Attachable"]
    # ingress = network.attrs["Ingress"]
    # config_from = network.attrs["ConfigFrom"]
    # config_only = network.attrs["ConfigOnly"]
    # containers = network.attrs["Containers"]
    # options = network.attrs["Options"]
    # labels = network.attrs["Labels"]
    assert key is not None
    assert name is not None
    assert labels is not None
    return NetworkInfo(key, name, labels)


class DockerNetwork(DockerBase):
    async def networks(
        self, filters: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[NetworkInfo]:
        updated_kwargs = dict()
        updated_kwargs.update(kwargs)
        if filters:
            updated_kwargs["filters"] = filters
        networks = self.docker.networks.list(**updated_kwargs)
        return [_create_network_info(n) for n in networks]

    def _get_network(self, key: str) -> Network:
        return self.docker.networks.get(key)

    async def exist_network(self, key: str) -> bool:
        try:
            return self._get_network(key) is not None
        except:  # noqa
            return False

    async def create_network(self, name: str, **kwargs) -> NetworkInfo:
        network = self.docker.networks.create(name, **kwargs)
        return _create_network_info(network)

    async def remove_network(self, key: str) -> None:
        self._get_network(key).remove()

    async def connect_network(self, key: str, container_key: str) -> None:
        self._get_network(key).connect(container_key)

    async def disconnect_network(
        self, key: str, container_key: str, force=False
    ) -> None:
        self._get_network(key).disconnect(container_key, force=force)
