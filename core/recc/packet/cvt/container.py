# -*- coding: utf-8 -*-

from typing import Dict, List
from recc.packet.container import ContainerA
from recc.container.struct.container_info import ContainerInfo


def container_to_answer(container: ContainerInfo) -> ContainerA:
    ports: Dict[str, List[str]] = dict()
    for key, value in container.ports.items():
        if str(key) not in ports:
            ports[str(key)] = list()
        ports[str(key)].append(str(value))
    return ContainerA(
        key=container.key,
        name=container.name,
        status=container.status.name,
        image=container.image,
        created=container.created,
        labels=container.labels,
        ports=ports,
    )
