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
    ) -> int:
        return await self.database.insert_permission(
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

    async def get_permission(self, uid: int) -> Permission:
        return await self.database.select_permission_by_uid(uid)

    async def get_permissions(self) -> List[Permission]:
        return await self.database.select_permissions()

    async def get_group_permission(self, user_uid: int, group_uid: int) -> Permission:
        return await self.database.select_permission_by_user_uid_and_group_uid(
            user_uid, group_uid
        )

    async def get_project_permission(
        self, user_uid: int, project_uid: int
    ) -> Permission:
        return await self.database.select_permission_by_user_uid_and_project_uid(
            user_uid, project_uid
        )

    async def get_best_permission(
        self, user_uid: int, group_uid: int, project_uid: int
    ) -> Permission:
        try:
            return await self.get_project_permission(user_uid, project_uid)
        except:  # noqa
            return await self.get_group_permission(user_uid, group_uid)
