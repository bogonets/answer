# -*- coding: utf-8 -*-

from typing import List, Dict
from recc.container.struct.container_status import ContainerStatus
from recc.container.struct.port_binding_host import PortBindingHost
from recc.container.struct.port_binding_guest import PortBindingGuest


class ContainerInfo:

    __slots__ = (
        "key",
        "name",
        "status",
        "image",
        "created",
        "labels",
        "ports",
    )

    key: str
    name: str
    status: ContainerStatus
    image: str
    created: str
    labels: Dict[str, str]
    ports: Dict[PortBindingGuest, List[PortBindingHost]]

    def __init__(
        self,
        key: str,
        name: str,
        status: ContainerStatus,
        image: str,
        created: str,
        labels: Dict[str, str],
        ports: Dict[PortBindingGuest, List[PortBindingHost]],
    ):
        self.key = key
        self.name = name
        if isinstance(status, str):
            self.status = ContainerStatus.from_str(status)
        elif isinstance(status, int):
            self.status = ContainerStatus(status)
        elif isinstance(status, ContainerStatus):
            self.status = status
        else:
            raise TypeError(f"Unsupported status type: {type(status).__name__}")
        self.image = image
        self.created = created
        self.labels = labels
        self.ports = ports
