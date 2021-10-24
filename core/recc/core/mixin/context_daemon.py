# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.daemon import Daemon


class ContextDaemon(ContextBase):
    async def create_daemon(
        self,
        plugin: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        requirements_sha256: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        enable: Optional[bool] = None,
    ) -> int:
        return await self.database.insert_daemon(
            plugin=plugin,
            name=name,
            address=address,
            requirements_sha256=requirements_sha256,
            description=description,
            extra=extra,
            enable=enable,
        )

    async def update_daemon(
        self,
        uid: int,
        plugin: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        requirements_sha256: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        enable: Optional[bool] = None,
    ) -> None:
        await self.database.update_daemon_by_uid(
            uid=uid,
            plugin=plugin,
            name=name,
            address=address,
            requirements_sha256=requirements_sha256,
            description=description,
            extra=extra,
            enable=enable,
        )

    async def delete_daemon(self, uid: int) -> None:
        await self.database.delete_daemon_by_uid(uid)

    async def get_daemon(self, uid: int) -> Daemon:
        return await self.database.select_daemon_by_uid(uid)

    async def get_daemons(self) -> List[Daemon]:
        return await self.database.select_daemons()
