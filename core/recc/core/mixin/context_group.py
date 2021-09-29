# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.group import Group
from recc.database.struct.group_member import GroupMember
from recc.database.struct.group_join_member import GroupJoinGroupMember
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE, VISIBILITY_LEVEL_INTERNAL


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
            owner_permission_uid = self.database.get_owner_permission_uid()
            await self.database.insert_group_member(
                group_uid, owner_uid, owner_permission_uid
            )
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

    async def get_groups_for_accessible(self, remove_sensitive=True) -> List[Group]:
        groups = await self.database.select_groups_by_below_visibility(
            VISIBILITY_LEVEL_INTERNAL
        )
        if remove_sensitive:
            for group in groups:
                group.remove_sensitive()
        return groups

    async def get_groups_by_user(
        self,
        user_uid: int,
        remove_sensitive=True,
    ) -> List[GroupJoinGroupMember]:
        groups = await self.database.select_group_members_join_group_by_user_uid(
            user_uid
        )
        if remove_sensitive:
            for group in groups:
                group.remove_sensitive()
        return groups

    async def get_group_members(self, group_uid: int) -> List[GroupMember]:
        return await self.database.select_group_members_by_group_uid(group_uid)

    async def get_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        return await self.database.select_group_member(group_uid, user_uid)

    async def add_group_member(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        return await self.database.insert_group_member(
            group_uid=group_uid,
            user_uid=user_uid,
            permission_uid=permission_uid,
        )

    async def update_group_member(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        return await self.database.update_group_member_permission(
            group_uid=group_uid,
            user_uid=user_uid,
            permission_uid=permission_uid,
        )

    async def remove_group_member(self, group_uid: int, user_uid: int) -> None:
        await self.database.delete_group_member(group_uid, user_uid)
