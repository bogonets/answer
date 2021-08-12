# -*- coding: utf-8 -*-

from typing import List
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.info import Info
from recc.rule.database_info import (
    valid_user_creatable,
    valid_user_modifiable,
    valid_user_removable,
)


class ContextInfo(ContextBase):
    async def create_info(self, key: str, val: str, force=False) -> None:
        if not force and not valid_user_creatable(key):
            raise KeyError(f"Non-creatable info: {key}")
        await self.database.create_info(key, val)

    async def update_info(self, key: str, val: str, force=False) -> None:
        if not force and not valid_user_modifiable(key):
            raise KeyError(f"Non-modifiable info: {key}")
        await self.database.update_info_value_by_key(key, val)

    async def delete_info(self, key: str, force=False) -> None:
        if not force and not valid_user_removable(key):
            raise KeyError(f"Non-removable info: {key}")
        await self.database.delete_info_by_key(key)

    async def get_infos(self) -> List[Info]:
        return await self.database.get_infos()

    async def get_info(self, key: str) -> Info:
        return await self.database.get_info_by_key(key)
