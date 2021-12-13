# -*- coding: utf-8 -*-

from typing import List, Optional, Any, Union
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.role import Role
from recc.packet.role import RawRole
from recc.packet.cvt.role import role_to_raw
from recc.session.session_ex import SessionEx


class ContextRole(ContextBase):
    async def create_role(
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
        role_uid = await self.database.insert_role(
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
        await self.cache.set_role(slug, role_uid)
        return role_uid

    @staticmethod
    def _is_role_equals_for_update(
        role: Role,
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
        """
        When role is 'locked', all attributes except `lock` must not be changed.
        """

        if slug is not None:
            if role.slug != slug:
                return False
        if name is not None:
            if role.name != name:
                return False
        if description is not None:
            if role.description != description:
                return False
        if features is not None:
            if role.features != features:
                return False
        if extra is not None:
            if role.extra != extra:
                return False
        if r_layout is not None:
            if role.r_layout != r_layout:
                return False
        if w_layout is not None:
            if role.w_layout != w_layout:
                return False
        if r_storage is not None:
            if role.r_storage != r_storage:
                return False
        if w_storage is not None:
            if role.w_storage != w_storage:
                return False
        if r_manager is not None:
            if role.r_manager != r_manager:
                return False
        if w_manager is not None:
            if role.w_manager != w_manager:
                return False
        if r_graph is not None:
            if role.r_graph != r_graph:
                return False
        if w_graph is not None:
            if role.w_graph != w_graph:
                return False
        if r_member is not None:
            if role.r_member != r_member:
                return False
        if w_member is not None:
            if role.w_member != w_member:
                return False
        if r_setting is not None:
            if role.r_setting != r_setting:
                return False
        if w_setting is not None:
            if role.w_setting != w_setting:
                return False
        if hidden is not None:
            if role.hidden != hidden:
                return False
        return True

    async def update_role(
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
            role = await self.database.select_role_by_uid(uid)
            if role.lock:
                role_equals = self._is_role_equals_for_update(
                    role,
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
                if not role_equals:
                    raise RuntimeError(f"Locked role: {uid}")

        await self.database.update_role_by_uid(
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
            await self.cache.remove_role_by_uid(uid)
            await self.cache.set_role(slug, uid)

    async def delete_role(self, uid: int, force=False) -> None:
        if not force:
            if await self.database.select_role_lock_by_uid(uid):
                raise RuntimeError(f"Locked role: {uid}")
        await self.database.delete_role_by_uid(uid)
        await self.cache.remove_role_by_uid(uid)

    async def get_role(self, uid: int) -> Role:
        return await self.database.select_role_by_uid(uid)

    async def get_roles(self) -> List[Role]:
        return await self.database.select_role_all()

    async def get_group_role(self, user_uid: int, group_uid: int) -> Role:
        return await self.database.select_role_by_user_uid_and_group_uid(
            user_uid, group_uid
        )

    async def get_project_role(self, user_uid: int, project_uid: int) -> Role:
        return await self.database.select_role_by_user_uid_and_project_uid(
            user_uid, project_uid
        )

    async def get_best_role(
        self, user_uid: int, group_uid: int, project_uid: int
    ) -> Role:
        try:
            return await self.get_project_role(user_uid, project_uid)
        except:  # noqa
            return await self.get_group_role(user_uid, group_uid)

    async def get_group_raw_role(
        self, session: SessionEx, group: Union[str, int]
    ) -> RawRole:
        try:
            if isinstance(group, int):
                group_uid = group
            elif isinstance(group, str):
                group_uid = await self.get_group_uid(group)
            else:
                group_uid = await self.get_group_uid(str(group))

            role = await self.get_group_role(session.uid, group_uid)
            return role_to_raw(role, session.is_admin)
        except:  # noqa
            if session.is_admin:
                return RawRole.all_true()
            else:
                return RawRole.all_false()

    async def get_project_raw_role(
        self, session: SessionEx, group: Union[str, int], project: Union[str, int]
    ) -> RawRole:
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

            role = await self.get_best_role(session.uid, group_uid, project_uid)
            return role_to_raw(role, session.is_admin)
        except:  # noqa
            if session.is_admin:
                return RawRole.all_true()
            else:
                return RawRole.all_false()
