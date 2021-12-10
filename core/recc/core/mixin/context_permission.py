# -*- coding: utf-8 -*-

from typing import List, Optional, Any, Union
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.permission import Permission
from recc.packet.permission import RawPermission
from recc.packet.cvt.permission import permission_to_raw
from recc.session.session_ex import SessionEx


class ContextPermission(ContextBase):
    async def create_permission(
        self,
        slug: str,
        name: Optional[str] = None,
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
        hidden=False,
        lock=False,
    ) -> int:
        permission_uid = await self.database.insert_permission(
            slug=slug,
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
            hidden=hidden,
            lock=lock,
        )
        await self.cache.set_permission(slug, permission_uid)
        return permission_uid

    @staticmethod
    def _is_permission_equals_for_update(
        permission: Permission,
        slug: Optional[str] = None,
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
        hidden: Optional[bool] = None,
    ) -> bool:
        """When permission is 'locked',
        all attributes except `lock` must not be changed.
        """

        if slug is not None:
            if permission.slug != slug:
                return False
        if name is not None:
            if permission.name != name:
                return False
        if description is not None:
            if permission.description != description:
                return False
        if features is not None:
            if permission.features != features:
                return False
        if extra is not None:
            if permission.extra != extra:
                return False
        if r_layout is not None:
            if permission.r_layout != r_layout:
                return False
        if w_layout is not None:
            if permission.w_layout != w_layout:
                return False
        if r_storage is not None:
            if permission.r_storage != r_storage:
                return False
        if w_storage is not None:
            if permission.w_storage != w_storage:
                return False
        if r_manager is not None:
            if permission.r_manager != r_manager:
                return False
        if w_manager is not None:
            if permission.w_manager != w_manager:
                return False
        if r_graph is not None:
            if permission.r_graph != r_graph:
                return False
        if w_graph is not None:
            if permission.w_graph != w_graph:
                return False
        if r_member is not None:
            if permission.r_member != r_member:
                return False
        if w_member is not None:
            if permission.w_member != w_member:
                return False
        if r_setting is not None:
            if permission.r_setting != r_setting:
                return False
        if w_setting is not None:
            if permission.w_setting != w_setting:
                return False
        if hidden is not None:
            if permission.hidden != hidden:
                return False
        return True

    async def update_permission(
        self,
        uid: int,
        slug: Optional[str] = None,
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
        hidden: Optional[bool] = None,
        lock: Optional[bool] = None,
        force=False,
    ) -> None:
        if not force:
            permission = await self.database.select_permission_by_uid(uid)
            if permission.lock:
                permission_equals = self._is_permission_equals_for_update(
                    permission,
                    slug,
                    name,
                    description,
                    features,
                    extra,
                    r_layout,
                    w_layout,
                    r_storage,
                    w_storage,
                    r_manager,
                    w_manager,
                    r_graph,
                    w_graph,
                    r_member,
                    w_member,
                    r_setting,
                    w_setting,
                    hidden,
                )
                if not permission_equals:
                    raise RuntimeError(f"Locked permission: {uid}")

        await self.database.update_permission_by_uid(
            uid=uid,
            slug=slug,
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
            hidden=hidden,
            lock=lock,
        )
        if slug is not None:
            await self.cache.remove_permission_by_uid(uid)
            await self.cache.set_permission(slug, uid)

    async def delete_permission(self, uid: int, force=False) -> None:
        if not force:
            if await self.database.select_permission_lock_by_uid(uid):
                raise RuntimeError(f"Locked permission: {uid}")
        await self.database.delete_permission_by_uid(uid)
        await self.cache.remove_permission_by_uid(uid)

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

    async def get_group_raw_permission(
        self, session: SessionEx, group: Union[str, int]
    ) -> RawPermission:
        try:
            if isinstance(group, int):
                group_uid = group
            elif isinstance(group, str):
                group_uid = await self.get_group_uid(group)
            else:
                group_uid = await self.get_group_uid(str(group))

            permission = await self.get_group_permission(session.uid, group_uid)
            return permission_to_raw(permission, session.is_admin)
        except:  # noqa
            if session.is_admin:
                return RawPermission.all_true()
            else:
                return RawPermission.all_false()

    async def get_project_raw_permission(
        self, session: SessionEx, group: Union[str, int], project: Union[str, int]
    ) -> RawPermission:
        try:
            if isinstance(group, int):
                group_uid = group
            elif isinstance(group, str):
                group_uid = await self.get_group_uid(group)
            else:
                group_uid = await self.get_group_uid(str(group))

            if isinstance(project, int):
                project_uid = project
            elif isinstance(project, str):
                project_uid = await self.get_project_uid(group_uid, project)
            else:
                project_uid = await self.get_project_uid(group_uid, str(project))

            permission = await self.get_best_permission(
                session.uid, group_uid, project_uid
            )
            return permission_to_raw(permission, session.is_admin)
        except:  # noqa
            if session.is_admin:
                return RawPermission.all_true()
            else:
                return RawPermission.all_false()
