# -*- coding: utf-8 -*-

from typing import List, Optional, Any, Union, Dict, Set
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.role import Role
from recc.database.struct.permission import Permission
from recc.database.struct.role_permission import RolePermission
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
        permissions: Optional[List[str]] = None,
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
        if permissions:
            # TODO: Merge into a single query
            await self.database.insert_role_permissions_by_slug(slug, permissions)
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
        permissions: Optional[List[str]] = None,
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
            # TODO: Merge into a single operation
            await self.cache.remove_role_by_uid(uid)
            await self.cache.set_role(slug, uid)

        if permissions is not None:
            # TODO: Merge into a single query
            await self.database.update_role_permissions_by_slug(uid, permissions)

    async def delete_role(self, uid: int, force=False) -> None:
        if not force:
            if await self.database.select_role_lock_by_uid(uid):
                raise RuntimeError(f"Locked role: {uid}")
        await self.database.delete_role_by_uid(uid)
        await self.cache.remove_role_by_uid(uid)

    async def get_permissions(self) -> List[Permission]:
        return await self.database.select_permission_all()

    async def get_permission_slugs_dict(self) -> Dict[int, str]:
        permissions = await self.get_permissions()
        result = dict()
        for p in permissions:
            assert p.uid is not None
            assert p.slug is not None
            result[p.uid] = p.slug
        return result

    async def get_role(self, uid: int) -> Role:
        return await self.database.select_role_by_uid(uid)

    async def get_roles(self) -> List[Role]:
        return await self.database.select_role_all()

    async def get_role_permissions(
        self, role_uid: Optional[int] = None
    ) -> List[RolePermission]:
        if role_uid is None:
            return await self.database.select_role_permission_all()
        else:
            return await self.database.select_role_permission_by_role_uid(role_uid)

    async def get_permission_slugs(self, role_uid: int) -> List[str]:
        permissions = await self.get_permission_slugs_dict()
        role_permissions = await self.get_role_permissions(role_uid)
        result = list()
        for rp in role_permissions:
            assert rp.permission_uid is not None
            result.append(permissions[rp.permission_uid])
        return result

    async def get_role_permissions_dict(self) -> Dict[int, Set[int]]:
        result: Dict[int, Set[int]] = dict()
        role_permissions = await self.get_role_permissions()
        for rp in role_permissions:
            assert rp.role_uid is not None
            assert rp.permission_uid is not None
            if rp.role_uid not in result:
                result[rp.role_uid] = set()
            result[rp.role_uid].add(rp.permission_uid)
        return result

    async def get_role_permission_slugs_dict(self) -> Dict[int, List[str]]:
        permissions = await self.get_permission_slugs_dict()
        role_permissions = await self.get_role_permissions_dict()
        result = dict()
        for role_uid, permission_uids in role_permissions.items():
            p_slugs = [permissions[p_uid] for p_uid in permission_uids]
            result[role_uid] = p_slugs
        return result

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
        if isinstance(group, int):
            group_uid = group
        elif isinstance(group, str):
            group_uid = await self.get_group_uid(group)
        else:
            group_uid = await self.get_group_uid(str(group))

        return await self.database.select_appropriate_permission_by_user_and_group(
            session.uid, group_uid
        )

    async def get_project_permission(
        self, session: SessionEx, group: Union[str, int], project: Union[str, int]
    ) -> List[Permission]:
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

        # fmt:off
        return await self.database.select_appropriate_permission_by_user_and_group_and_project(  # noqa
            session.uid, group_uid, project_uid
        )
        # fmt:on

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
