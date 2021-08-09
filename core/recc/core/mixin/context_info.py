# -*- coding: utf-8 -*-

from typing import List, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.info import Info
from recc.rule.database_info import valid_user_modifiable, valid_user_removable


class ContextInfo(ContextBase):
    async def get_infos(self) -> List[Info]:
        infos = await self.database.get_infos()
        return [Info(i.key, i.value) for i in infos]

    async def get_info(self, key: str) -> Info:
        info = await self.database.get_info_by_key(key)
        return Info(info.key, info.value)

    async def set_info(self, key: str, val: Any, force=False) -> None:
        if not force and not valid_user_modifiable(key):
            raise KeyError(f"Non-modifiable info key: {key}")
        await self.database.upsert_info(key, val)

    async def delete_info(self, key: str, force=False) -> None:
        if not force and not valid_user_removable(key):
            raise KeyError(f"Non-removable info key: {key}")
        await self.database.delete_info_by_key(key)
