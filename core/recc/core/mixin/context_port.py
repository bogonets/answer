# -*- coding: utf-8 -*-

from typing import Optional
from recc.core.mixin.context_base import ContextBase


class ContextPort(ContextBase):
    def _alloc_port(self, port: Optional[int]) -> None:
        if port is None:
            return

        try:
            self.ports.alloc(port, force=True)
        except:  # noqa
            pass

    async def update_ports_from_database(self) -> None:
        ports = await self.database.get_ports()
        for port in ports:
            self._alloc_port(port.number)

    async def update_ports_from_container(self) -> None:
        containers = await self.container.get_tasks()
        for container in containers:
            for guest, hosts in container.ports.items():
                for host in hosts:
                    self._alloc_port(host.port)
