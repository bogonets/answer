# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from recc.variables.database import (
    PERMISSION_SLUG_RECC_LAYOUT_READ,
    PERMISSION_SLUG_RECC_LAYOUT_WRITE,
    PERMISSION_SLUG_RECC_STORAGE_READ,
    PERMISSION_SLUG_RECC_STORAGE_WRITE,
    PERMISSION_SLUG_RECC_MANAGER_READ,
    PERMISSION_SLUG_RECC_MANAGER_WRITE,
    PERMISSION_SLUG_RECC_GRAPH_READ,
    PERMISSION_SLUG_RECC_GRAPH_WRITE,
    PERMISSION_SLUG_RECC_MEMBER_READ,
    PERMISSION_SLUG_RECC_MEMBER_WRITE,
    PERMISSION_SLUG_RECC_SETTING_READ,
    PERMISSION_SLUG_RECC_SETTING_WRITE,
)


class PgPermissionTestCase(PostgresqlTestCase):
    async def test_default_permissions(self):
        perms = await self.db.select_permission_all()
        slugs = [p.slug for p in perms]
        self.assertIn(PERMISSION_SLUG_RECC_LAYOUT_READ, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_LAYOUT_WRITE, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_STORAGE_READ, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_STORAGE_WRITE, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_MANAGER_READ, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_MANAGER_WRITE, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_GRAPH_READ, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_GRAPH_WRITE, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_MEMBER_READ, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_MEMBER_WRITE, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_SETTING_READ, slugs)
        self.assertIn(PERMISSION_SLUG_RECC_SETTING_WRITE, slugs)

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


if __name__ == "__main__":
    main()
