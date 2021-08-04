# -*- coding: utf-8 -*-

from typing import List, Any
from recc.core.mixin.context_base import ContextBase


class Config:

    __slots__ = ("key", "val")

    key: str
    val: Any

    def __init__(self, key: str, val: Any):
        self.key = key
        self.val = val


class ContextConfig(ContextBase):
    async def get_configs(self) -> List[Config]:
        infos = await self.database.get_infos()
        return [Config(i.key, i.value) for i in infos]

    async def get_config(self, key: str) -> Config:
        info = await self.database.get_info_by_key(key)
        return Config(info.key, info.value)

    async def set_config(self, key: str, val: Any) -> None:
        await self.database.upsert_info(key, val)