# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.group import Group
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


class ContextGroup(ContextBase):
    async def create_group(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility=VISIBILITY_LEVEL_PRIVATE,
        extra: Any = None,
        owner_uid: Optional[int] = None,
    ) -> int:
        group_uid = await self.database.insert_group(
            slug=slug,
            name=name,
            description=description,
            features=features,
            visibility=visibility,
            extra=extra,
        )
        if owner_uid is not None:
            permission_uid = self.database.get_maintainer_permission_uid()
            self.database.insert_group_member(group_uid, owner_uid, permission_uid)
        return group_uid

    async def update_group(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility: Optional[int] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_group_by_uid(
            uid=uid,
            slug=slug,
            name=name,
            description=description,
            features=features,
            visibility=visibility,
            extra=extra,
        )

    async def delete_group(self, uid: int) -> None:
        await self.database.delete_group_by_uid(uid)

    async def get_group(self, uid: int, remove_sensitive=True) -> Group:
        result = await self.database.select_group_by_uid(uid)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_groups(self, remove_sensitive=True) -> List[Group]:
        groups = await self.database.select_groups()
        if remove_sensitive:
            for group in groups:
                group.remove_sensitive()
        return groups
