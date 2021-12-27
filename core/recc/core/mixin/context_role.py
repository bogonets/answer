# -*- coding: utf-8 -*-

from typing import List, Optional, Any, Union
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.role import Role
from recc.database.struct.permission import Permission
from recc.session.session_ex import SessionEx


class ContextRole(ContextBase):
    async def create_role(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        hidden=False,
        lock=False,
    ) -> int:
        role_uid = await self.database.insert_role(
            slug=slug,
            name=name,
            description=description,
            extra=extra,
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
        extra: Optional[Any] = None,
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
        if extra is not None:
            if role.extra != extra:
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
        extra: Optional[Any] = None,
        hidden: Optional[bool] = None,
        lock: Optional[bool] = None,
        force=False,
    ) -> None:
        if not force:
            role = await self.database.select_role_by_uid(uid)
            if role.lock:
                role_equals = self._is_role_equals_for_update(
                    role, slug, name, description, extra, hidden
                )
                if not role_equals:
                    raise RuntimeError(f"Locked role: {uid}")

        await self.database.update_role_by_uid(
            uid=uid,
            slug=slug,
            name=name,
            description=description,
            extra=extra,
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

    async def get_group_permission(
        self, session: SessionEx, group: Union[str, int]
    ) -> List[Permission]:
        if session.is_admin:
            return await self.database.select_permission_all()

        if isinstance(group, int):
            group_uid = group
        elif isinstance(group, str):
            group_uid = await self.get_group_uid(group)
        else:
            group_uid = await self.get_group_uid(str(group))

        return await self.database.select_permission_by_user_and_group(
            session.uid, group_uid
        )

    async def get_project_permission(
        self, session: SessionEx, group: Union[str, int], project: Union[str, int]
    ) -> List[Permission]:
        if session.is_admin:
            return await self.database.select_permission_all()

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

        return await self.database.select_permission_by_user_and_group(
            session.uid, project_uid
        )

    @staticmethod
    def _verify_permissions(
        required_permissions: List[Union[int, str]],
        have_permissions: List[Permission],
    ) -> None:
        uid_perms = set(map(lambda x: x.uid, have_permissions))
        slug_perms = set(map(lambda x: x.slug, have_permissions))

        for perm in required_permissions:
            if isinstance(perm, int):
                if perm not in uid_perms:
                    raise PermissionError(f"Permission denied: Not have {perm}")
            else:
                assert isinstance(perm, str)
                if perm not in slug_perms:
                    raise PermissionError(f'Permission denied: Not have "{perm}"')

    async def verify_group_permissions(
        self,
        session: SessionEx,
        group: Union[str, int],
        required_permissions: List[Union[int, str]],
    ) -> None:
        have_permissions = await self.get_group_permission(session, group)
        self._verify_permissions(required_permissions, have_permissions)

    async def verify_project_permissions(
        self,
        session: SessionEx,
        group: Union[str, int],
        project: Union[str, int],
        required_permissions: List[Union[int, str]],
    ) -> None:
        have_permissions = await self.get_project_permission(session, group, project)
        self._verify_permissions(required_permissions, have_permissions)
