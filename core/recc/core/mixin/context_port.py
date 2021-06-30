# -*- coding: utf-8 -*-

from recc.core.mixin.context_base import ContextBase


class ContextPort(ContextBase):
    async def update_from_database(self) -> None:
        ports = await self.database.get_ports()
        for port in ports:
            if port.number:
                self.ports.alloc(port.number, force=True)

    async def update_from_container(self) -> None:
        pass
