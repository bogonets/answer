# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from recc.variables.database import (
    DEFAULT_PERMISSION_SLUGS,
    DEFAULT_ROLE_SLUGS,
    ROLE_SLUG_OWNER,
    ROLE_SLUG_MAINTAINER,
    ROLE_SLUG_DEVELOPER,
    ROLE_SLUG_REPORTER,
    ROLE_SLUG_GUEST,
    PERMISSIONS_OF_OWNER,
    PERMISSIONS_OF_MAINTAINER,
    PERMISSIONS_OF_DEVELOPER,
    PERMISSIONS_OF_REPORTER,
    PERMISSIONS_OF_GUEST,
)


class PgPermissionTestCase(PostgresqlTestCase):
    async def test_default_permissions(self):
        for parm in await self.db.select_permission_all():
            self.assertIn(parm.slug, DEFAULT_PERMISSION_SLUGS)
        for role in await self.db.select_role_all():
            self.assertIn(role.slug, DEFAULT_ROLE_SLUGS)

    async def test_insert_and_delete(self):
        perm_slug = "test.insert.and.delete"
        perm_uid = await self.db.insert_permission(perm_slug)
        slugs1 = [p.slug for p in await self.db.select_permission_all()]
        self.assertIn(perm_slug, slugs1)

        await self.db.delete_permission(perm_uid)
        slugs2 = [p.slug for p in await self.db.select_permission_all()]
        self.assertNotIn(perm_slug, slugs2)

    async def test_select(self):
        perm_slug1 = "test.select"
        perm_uid1 = await self.db.insert_permission(perm_slug1)

        perm_uid2 = await self.db.select_permission_uid_by_slug(perm_slug1)
        perm_slug2 = await self.db.select_permission_slug_by_uid(perm_uid1)

        self.assertEqual(perm_slug1, perm_slug2)
        self.assertEqual(perm_uid1, perm_uid2)

        perm3 = await self.db.select_permission_by_slug(perm_slug1)
        self.assertEqual(perm_uid1, perm3.uid)
        self.assertEqual(perm_slug1, perm3.slug)

        perm4 = await self.db.select_permission_by_uid(perm_uid1)
        self.assertEqual(perm_uid1, perm4.uid)
        self.assertEqual(perm_slug1, perm4.slug)

    async def test_by_role_uid(self):
        owner_uid = await self.db.select_role_uid_by_slug(ROLE_SLUG_OWNER)
        maintainer_uid = await self.db.select_role_uid_by_slug(ROLE_SLUG_MAINTAINER)
        developer_uid = await self.db.select_role_uid_by_slug(ROLE_SLUG_DEVELOPER)
        reporter_uid = await self.db.select_role_uid_by_slug(ROLE_SLUG_REPORTER)
        guest_uid = await self.db.select_role_uid_by_slug(ROLE_SLUG_GUEST)

        owner = await self.db.select_permission_by_role_uid(owner_uid)
        maintainer = await self.db.select_permission_by_role_uid(maintainer_uid)
        developer = await self.db.select_permission_by_role_uid(developer_uid)
        reporter = await self.db.select_permission_by_role_uid(reporter_uid)
        guest = await self.db.select_permission_by_role_uid(guest_uid)

        owner_slugs = list(set(map(lambda x: x.slug, owner)))
        maintainer_slugs = list(set(map(lambda x: x.slug, maintainer)))
        developer_slugs = list(set(map(lambda x: x.slug, developer)))
        reporter_slugs = list(set(map(lambda x: x.slug, reporter)))
        guest_slugs = list(set(map(lambda x: x.slug, guest)))

        self.assertListEqual(owner_slugs, list(set(PERMISSIONS_OF_OWNER)))
        self.assertListEqual(maintainer_slugs, list(set(PERMISSIONS_OF_MAINTAINER)))
        self.assertListEqual(developer_slugs, list(set(PERMISSIONS_OF_DEVELOPER)))
        self.assertListEqual(reporter_slugs, list(set(PERMISSIONS_OF_REPORTER)))
        self.assertListEqual(guest_slugs, list(set(PERMISSIONS_OF_GUEST)))


if __name__ == "__main__":
    main()
