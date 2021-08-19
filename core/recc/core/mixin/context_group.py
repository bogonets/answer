# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.group import Group


class ContextGroup(ContextBase):
    async def create_group(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Any = None,
    ) -> None:
        await self.database.create_group(
            slug=slug,
            name=name,
            description=description,
            features=features,
            extra=extra,
        )

    async def update_group(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_group_by_uid(
            uid, slug, name, description, features, extra
        )

    async def delete_group(self, uid: int) -> None:
        await self.database.delete_group_by_uid(uid)

    async def get_group(self, uid: int, remove_sensitive=True) -> Group:
        result = await self.database.get_group_by_uid(uid)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_groups(self, remove_sensitive=True) -> List[Group]:
        groups = await self.database.get_groups()
        if remove_sensitive:
            for group in groups:
                group.remove_sensitive()
        return groups
