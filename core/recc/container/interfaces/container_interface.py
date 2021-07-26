# -*- coding: utf-8 -*-

from abc import ABCMeta
from recc.container.interfaces.container_container import ContainerContainer
from recc.container.interfaces.container_image import ContainerImage
from recc.container.interfaces.container_misc import ContainerMisc
from recc.container.interfaces.container_network import ContainerNetwork
from recc.container.interfaces.container_open import ContainerOpen
from recc.container.interfaces.container_task import ContainerTask
from recc.container.interfaces.container_volume import ContainerVolume


class ContainerInterface(
    ContainerContainer,
    ContainerImage,
    ContainerMisc,
    ContainerNetwork,
    ContainerOpen,
    ContainerTask,
    ContainerVolume,
    metaclass=ABCMeta,
):
    """
    Container Manager (OS-level virtualization) interface.
    """

    pass
