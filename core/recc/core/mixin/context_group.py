# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.group import Group


class ContextGroup(ContextBase):
    async def create_group(
        self,
        name: str,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Any = None,
    ) -> None:
        await self.database.create_group(
            name,
            description=description,
            features=features,
            extra=extra,
        )

    async def update_group_name(self, uid: int, name: str) -> None:
        await self.database.update_group_name_by_uid(uid, name)

    async def update_group_description_by_uid(self, uid: int, description: str) -> None:
        await self.database.update_group_description_by_uid(uid, description)

    async def update_group_description_by_name(
        self, name: str, description: str
    ) -> None:
        await self.database.update_group_description_by_name(name, description)

    async def update_group_extra_by_uid(self, uid: int, extra: Any) -> None:
        await self.database.update_group_extra_by_uid(uid, extra)

    async def update_group_extra_by_name(self, name: str, extra: Any) -> None:
        await self.database.update_group_extra_by_name(name, extra)

    async def update_group_features_by_uid(self, uid: int, features: List[str]) -> None:
        await self.database.update_group_features_by_uid(uid, features)

    async def update_group_features_by_name(
        self, name: str, features: List[str]
    ) -> None:
        await self.database.update_group_features_by_name(name, features)

    async def update_group_by_uid(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_group_by_uid(uid, name, description, features, extra)

    async def delete_group_by_uid(self, uid: int) -> None:
        await self.database.delete_group_by_uid(uid)

    async def delete_group_by_name(self, name: str) -> None:
        await self.database.delete_group_by_name(name)

    async def get_group_uid_by_name(self, name: str) -> int:
        return await self.database.get_group_uid_by_name(name)

    async def get_group_by_uid(self, uid: int, remove_sensitive=True) -> Group:
        result = await self.database.get_group_by_uid(uid)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_group_by_name(self, name: str, remove_sensitive=True) -> Group:
        result = await self.database.get_group_by_name(name)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_groups(self, remove_sensitive=True) -> List[Group]:
        groups = await self.database.get_groups()
        if remove_sensitive:
            for group in groups:
                group.remove_sensitive()
        return groups
