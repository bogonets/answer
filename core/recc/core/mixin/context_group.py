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

    async def get_group_uid(self, slug: str, caching=True) -> int:
        if not slug:
            raise ValueError("The `slug` argument is empty.")
        uid = self.cache.get_group_uid(slug)
        if uid is None:
            uid = await self.database.get_group_uid_by_slug(slug)
            if caching:
                self.cache.set_group(uid, slug)
        return uid

    async def get_group_slug(self, uid: int, caching=True) -> str:
        slug = self.cache.get_group_slug(uid)
        if slug is None:
            slug = await self.database.get_group_slug_by_uid(uid)
            if caching:
                self.cache.set_group(uid, slug)
        return slug

    async def update_group_slug(self, uid: int, slug: str) -> None:
        await self.database.update_group_slug_by_uid(uid, slug)

    async def update_group_description_by_uid(self, uid: int, description: str) -> None:
        await self.database.update_group_description_by_uid(uid, description)

    async def update_group_description_by_slug(
        self, slug: str, description: str
    ) -> None:
        await self.database.update_group_description_by_slug(slug, description)

    async def update_group_extra_by_uid(self, uid: int, extra: Any) -> None:
        await self.database.update_group_extra_by_uid(uid, extra)

    async def update_group_extra_by_slug(self, slug: str, extra: Any) -> None:
        await self.database.update_group_extra_by_slug(slug, extra)

    async def update_group_features_by_uid(self, uid: int, features: List[str]) -> None:
        await self.database.update_group_features_by_uid(uid, features)

    async def update_group_features_by_slug(
        self, slug: str, features: List[str]
    ) -> None:
        await self.database.update_group_features_by_slug(slug, features)

    async def update_group_by_uid(
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

    async def update_group_by_slug(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_group_by_slug(
            slug, name, description, features, extra
        )

    async def delete_group_by_uid(self, uid: int) -> None:
        await self.database.delete_group_by_uid(uid)

    async def delete_group_by_slug(self, slug: str) -> None:
        await self.database.delete_group_by_slug(slug)

    async def get_group_uid_by_slug(self, slug: str) -> int:
        return await self.database.get_group_uid_by_slug(slug)

    async def get_group_by_uid(self, uid: int, remove_sensitive=True) -> Group:
        result = await self.database.get_group_by_uid(uid)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_group_by_slug(self, slug: str, remove_sensitive=True) -> Group:
        result = await self.database.get_group_by_slug(slug)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_groups(self, remove_sensitive=True) -> List[Group]:
        groups = await self.database.get_groups()
        if remove_sensitive:
            for group in groups:
                group.remove_sensitive()
        return groups
