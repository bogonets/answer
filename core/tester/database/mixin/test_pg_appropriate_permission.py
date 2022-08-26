# -*- coding: utf-8 -*-

from typing import List
from unittest import main

from recc.packet.permission import Permission
from recc.variables.database import (
    ROLE_SLUG_DEVELOPER,
    ROLE_SLUG_GUEST,
    ROLE_SLUG_MAINTAINER,
    ROLE_SLUG_OWNER,
    ROLE_SLUG_REPORTER,
)
from tester.unittest.postgresql_test_case import PostgresqlTestCase


def _permission_slugs(perms: List[Permission]) -> List[str]:
    return list(set(p.slug for p in perms if p.slug))


class PgAppropriatePermissionTestCase(PostgresqlTestCase):
    async def _group_perms(self, user_uid: int, group_uid: int) -> List[str]:
        perms = await self.db.select_appropriate_permission_by_user_and_group(
            user_uid, group_uid
        )
        return _permission_slugs(perms)

    async def _project_perms(
        self, user_uid: int, group_uid: int, project_uid: int
    ) -> List[str]:
        perms = (
            await self.db.select_appropriate_permission_by_user_and_group_and_project(
                user_uid, group_uid, project_uid
            )
        )
        return _permission_slugs(perms)

    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.user1 = await self.db.insert_user("user1", "p", "s")
        self.user2 = await self.db.insert_user("user2", "p", "s")
        self.user3 = await self.db.insert_user("user3", "p", "s")

        owner = await self.db.select_role_uid_by_slug(ROLE_SLUG_OWNER)
        maintainer = await self.db.select_role_uid_by_slug(ROLE_SLUG_MAINTAINER)
        developer = await self.db.select_role_uid_by_slug(ROLE_SLUG_DEVELOPER)
        reporter = await self.db.select_role_uid_by_slug(ROLE_SLUG_REPORTER)
        guest = await self.db.select_role_uid_by_slug(ROLE_SLUG_GUEST)

        admin_perms = await self.db.select_permission_all()
        owner_perms = await self.db.select_permission_by_role_uid(owner)
        maintainer_perms = await self.db.select_permission_by_role_uid(maintainer)
        developer_perms = await self.db.select_permission_by_role_uid(developer)
        reporter_perms = await self.db.select_permission_by_role_uid(reporter)
        guest_perms = await self.db.select_permission_by_role_uid(guest)

        self.admin = _permission_slugs(admin_perms)
        self.owner = _permission_slugs(owner_perms)
        self.maintainer = _permission_slugs(maintainer_perms)
        self.developer = _permission_slugs(developer_perms)
        self.reporter = _permission_slugs(reporter_perms)
        self.guest = _permission_slugs(guest_perms)

        self.group1 = await self.db.insert_group("group1")
        await self.db.insert_group_member(self.group1, self.user1, owner)
        await self.db.insert_group_member(self.group1, self.user2, maintainer)

        self.project1 = await self.db.insert_project(self.group1, "project1")
        await self.db.insert_project_member(self.project1, self.user1, reporter)
        await self.db.insert_project_member(self.project1, self.user2, owner)
        await self.db.insert_project_member(self.project1, self.user3, developer)

        self.group2 = await self.db.insert_group("group2")
        await self.db.insert_group_member(self.group2, self.user2, owner)
        await self.db.insert_group_member(self.group2, self.user3, developer)

        self.project2 = await self.db.insert_project(self.group2, "project2")
        await self.db.insert_project_member(self.project2, self.user1, guest)
        await self.db.insert_project_member(self.project2, self.user2, owner)

    async def test_admin(self):
        user0 = await self.db.insert_user("user0", "p", "s", admin=True)
        perms1 = await self._group_perms(user0, self.group1)
        perms2 = await self._project_perms(user0, self.group1, self.project1)
        perms3 = await self._group_perms(user0, self.group2)
        perms4 = await self._project_perms(user0, self.group2, self.project2)
        self.assertListEqual(self.admin, perms1)
        self.assertListEqual(self.admin, perms2)
        self.assertListEqual(self.admin, perms3)
        self.assertListEqual(self.admin, perms4)

    async def test_default(self):
        perms1 = await self._group_perms(self.user1, self.group1)
        perms2 = await self._group_perms(self.user2, self.group1)
        perms3 = await self._group_perms(self.user3, self.group1)
        self.assertListEqual(self.owner, perms1)
        self.assertListEqual(self.maintainer, perms2)
        self.assertFalse(perms3)

        perms4 = await self._project_perms(self.user1, self.group1, self.project1)
        perms5 = await self._project_perms(self.user2, self.group1, self.project1)
        perms6 = await self._project_perms(self.user3, self.group1, self.project1)
        self.assertListEqual(self.reporter, perms4)
        self.assertListEqual(self.owner, perms5)
        self.assertListEqual(self.developer, perms6)

        perms7 = await self._group_perms(self.user1, self.group2)
        perms8 = await self._group_perms(self.user2, self.group2)
        perms9 = await self._group_perms(self.user3, self.group2)
        self.assertFalse(perms7)
        self.assertListEqual(self.owner, perms8)
        self.assertListEqual(self.developer, perms9)

        perms10 = await self._project_perms(self.user1, self.group2, self.project2)
        perms11 = await self._project_perms(self.user2, self.group2, self.project2)
        perms12 = await self._project_perms(self.user3, self.group2, self.project2)
        self.assertListEqual(self.guest, perms10)
        self.assertListEqual(self.owner, perms11)
        self.assertListEqual(self.developer, perms12)


if __name__ == "__main__":
    main()
