# -*- coding: utf-8 -*-

from typing import List, Dict
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.info import Info
from recc.rule.database_info import (
    valid_user_creatable,
    valid_user_modifiable,
    valid_user_removable,
)
from recc.variables.database import INFO_KEY_OEM


class ContextInfo(ContextBase):
    async def create_info(self, key: str, val: str, force=False) -> None:
        if not force and not valid_user_creatable(key):
            raise KeyError(f"Non-creatable info: {key}")
        await self.database.insert_info(key, val)

    async def update_info(self, key: str, val: str, force=False) -> None:
        if not force and not valid_user_modifiable(key):
            raise KeyError(f"Non-modifiable info: {key}")
        await self.database.update_info_value_by_key(key, val)

    async def delete_info(self, key: str, force=False) -> None:
        if not force and not valid_user_removable(key):
            raise KeyError(f"Non-removable info: {key}")
        await self.database.delete_info_by_key(key)

    async def get_infos(self) -> List[Info]:
        return await self.database.select_infos()

    async def get_infos_as_dict(self) -> Dict[str, str]:
        infos = await self.get_infos()
        result = dict()
        for info in infos:
            if not info.key:
                continue
            result[info.key] = info.value if info.value else str()
        return result

    async def get_infos_like(self, like: str) -> List[Info]:
        return await self.database.select_infos_like(like)

    async def get_info(self, key: str) -> Info:
        return await self.database.select_info_by_key(key)

    async def opt_info_str(self, key: str, default_value="") -> str:
        try:
            info = await self.get_info(key)
            if info.value is not None:
                return info.value
            else:
                return default_value
        except:  # noqa
            return default_value

    async def opt_info_bool(self, key: str, default_value=False) -> bool:
        try:
            info = await self.get_info(key)
            if info.value is not None:
                return bool(info.value)
            else:
                return default_value
        except:  # noqa
            return default_value

    async def opt_info_int(self, key: str, default_value=0) -> int:
        try:
            info = await self.get_info(key)
            if info.value is not None:
                return int(info.value)
            else:
                return default_value
        except:  # noqa
            return default_value

    async def opt_info_float(self, key: str, default_value=0.0) -> float:
        try:
            info = await self.get_info(key)
            if info.value is not None:
                return float(info.value)
            else:
                return default_value
        except:  # noqa
            return default_value

    async def get_info_oem(self) -> Info:
        return await self.get_info(INFO_KEY_OEM)

    async def opt_info_oem_value(self, default_value="") -> str:
        try:
            info = await self.get_info(INFO_KEY_OEM)
            if info.value:
                return info.value
            else:
                return default_value
        except:  # noqa
            return default_value

    async def set_info_oem(self, value: str) -> Info:
        return await self.database.upsert_info(INFO_KEY_OEM, value)
