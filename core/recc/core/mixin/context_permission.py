# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.permission import Permission


class ContextPermission(ContextBase):
    async def create_permission(
        self,
        name: str,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout=False,
        w_layout=False,
        r_storage=False,
        w_storage=False,
        r_manager=False,
        w_manager=False,
        r_graph=False,
        w_graph=False,
        r_member=False,
        w_member=False,
        r_setting=False,
        w_setting=False,
    ) -> None:
        await self.database.create_permission(
            name=name,
            description=description,
            features=features,
            extra=extra,
            r_layout=r_layout,
            w_layout=w_layout,
            r_storage=r_storage,
            w_storage=w_storage,
            r_manager=r_manager,
            w_manager=w_manager,
            r_graph=r_graph,
            w_graph=w_graph,
            r_member=r_member,
            w_member=w_member,
            r_setting=r_setting,
            w_setting=w_setting,
        )

    async def get_permission_uid(self, name: str, caching=True) -> int:
        if not name:
            raise ValueError("The `name` argument is empty.")
        uid = self.cache.get_permission_uid(name)
        if uid is None:
            uid = await self.database.get_permission_uid_by_name(name)
            if caching:
                self.cache.set_permission(uid, name)
        return uid

    async def get_permission_name(self, uid: int, caching=True) -> str:
        slug = self.cache.get_permission_name(uid)
        if slug is None:
            slug = await self.database.get_permission_name_by_uid(uid)
            if caching:
                self.cache.set_permission(uid, slug)
        return slug

    async def update_permission(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout: Optional[bool] = None,
        w_layout: Optional[bool] = None,
        r_storage: Optional[bool] = None,
        w_storage: Optional[bool] = None,
        r_manager: Optional[bool] = None,
        w_manager: Optional[bool] = None,
        r_graph: Optional[bool] = None,
        w_graph: Optional[bool] = None,
        r_member: Optional[bool] = None,
        w_member: Optional[bool] = None,
        r_setting: Optional[bool] = None,
        w_setting: Optional[bool] = None,
    ) -> None:
        await self.database.update_permission_by_uid(
            uid=uid,
            name=name,
            description=description,
            features=features,
            extra=extra,
            r_layout=r_layout,
            w_layout=w_layout,
            r_storage=r_storage,
            w_storage=w_storage,
            r_manager=r_manager,
            w_manager=w_manager,
            r_graph=r_graph,
            w_graph=w_graph,
            r_member=r_member,
            w_member=w_member,
            r_setting=r_setting,
            w_setting=w_setting,
        )

    async def delete_permission(self, uid: int) -> None:
        await self.database.delete_permission_by_uid(uid)

    async def get_permission(self, uid: int, remove_sensitive=True) -> Permission:
        result = await self.database.get_permission_by_uid(uid)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_permissions(self, remove_sensitive=True) -> List[Permission]:
        permissions = await self.database.get_permissions()
        if remove_sensitive:
            for permission in permissions:
                permission.remove_sensitive()
        return permissions
