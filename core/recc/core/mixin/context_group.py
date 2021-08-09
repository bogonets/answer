# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.group import Group


class ContextGroup(ContextBase):
    async def create_group(
        self,
        group_name: str,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Any = None,
    ) -> None:
        await self.database.create_group(
            group_name,
            description=description,
            features=features,
            extra=extra,
        )

    async def get_groups(self) -> List[Group]:
        return await self.database.get_groups()

    async def get_groups_by_name(self, group_name: str) -> List[Group]:
        group = await self.database.get_group_by_name(group_name)
        assert group.uid is not None
        return await self.get_groups(group.uid)

    async def delete_group(self, group_uid: int) -> None:
        await self.database.delete_group_by_uid(group_uid)
