# -*- coding: utf-8 -*-

from typing import List

from recc.core.mixin.context_base import ContextBase
from recc.packet.port import Port


class ContextPort(ContextBase):
    async def get_ports(self) -> List[Port]:
        return await self.database.select_port_all()

    async def get_port_numbers(self) -> List[int]:
        return await self.database.select_port_number_all()

    async def next_available_port_number(self) -> int:
        unavailable_numbers = set(await self.get_port_numbers())
        begin = self.config.manage_port_min
        end = self.config.manage_port_max
        assert begin < end
        while begin < end:
            if begin not in unavailable_numbers:
                return begin
            else:
                begin += 1
        raise IndexError("No port number available")

    # def _alloc_port(self, port: Optional[int]) -> None:
    #     if port is None:
    #         return
    #
    #     try:
    #         self.ports.alloc(port, force=True)
    #     except:  # noqa
    #         pass
    #
    # def get_port_range(self) -> Tuple[int, int]:
    #     return self.ports.range
    #
    # async def update_ports_from_database(self) -> None:
    #     ports = await self.database.select_ports()
    #     for port in ports:
    #         self._alloc_port(port.number)
    #
    # async def update_ports_from_container(self) -> None:
    #     containers = await self.container.get_tasks()
    #     for container in containers:
    #         for guest, hosts in container.ports.items():
    #             for host in hosts:
    #                 self._alloc_port(host.port)
