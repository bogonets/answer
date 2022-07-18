# -*- coding: utf-8 -*-

from typing import Any, List, Optional

from recc.core.mixin.context_base import ContextBase
from recc.packet.group import Group
from recc.packet.group_join_member import GroupJoinGroupMember
from recc.packet.group_member import GroupMember
from recc.variables.database import (
    ROLE_UID_OWNER,
    VISIBILITY_LEVEL_INTERNAL,
    VISIBILITY_LEVEL_PRIVATE,
)


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
        # TODO: merge single query.
        group_uid = await self.database.insert_group(
            slug=slug,
            name=name,
            description=description,
            features=features,
            visibility=visibility,
            extra=extra,
        )
        if owner_uid is not None:
            await self.database.insert_group_member(
                group_uid, owner_uid, ROLE_UID_OWNER
            )
        await self.cache.set_group(slug, group_uid)
        await self._plugins.on_create_group(group_uid)
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
        if slug is not None:
            await self.cache.remove_group_by_uid(uid)
            await self.cache.set_group(slug, uid)

    async def delete_group(self, uid: int) -> None:
        await self.database.delete_group_by_uid(uid)
        await self._plugins.on_delete_group(uid)
        # TODO: call on_delete_project() of all plugins
        await self.cache.remove_group_by_uid(uid)

    async def get_group(self, uid: int) -> Group:
        return await self.database.select_group_by_uid(uid)

    async def get_groups(self) -> List[Group]:
        return await self.database.select_groups()

    async def get_groups_for_accessible(self) -> List[Group]:
        return await self.database.select_groups_by_below_visibility(
            VISIBILITY_LEVEL_INTERNAL
        )

    async def get_groups_by_user(self, user_uid: int) -> List[GroupJoinGroupMember]:
        return await self.database.select_group_members_join_group_by_user_uid(user_uid)

    async def get_group_members(self, group_uid: int) -> List[GroupMember]:
        return await self.database.select_group_members_by_group_uid(group_uid)

    async def get_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        return await self.database.select_group_member(group_uid, user_uid)

    async def add_group_member(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        return await self.database.insert_group_member(
            group_uid=group_uid,
            user_uid=user_uid,
            role_uid=role_uid,
        )

    async def update_group_member(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        return await self.database.update_group_member_role(
            group_uid=group_uid,
            user_uid=user_uid,
            role_uid=role_uid,
        )

    async def remove_group_member(self, group_uid: int, user_uid: int) -> None:
        await self.database.delete_group_member(group_uid, user_uid)
