# -*- coding: utf-8 -*-

from unittest import main

from recc.database.postgresql.query.role_permission import (
    safe_insert_role_permission_by_slug,
)
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgRolePermissionTestCase(PostgresqlTestCase):
    async def test_safe_insert(self):
        perm1_slug = "test.perm1"
        role1_slug = "role1"
        await self.db.insert_permission(perm1_slug)
        role1_uid = await self.db.insert_role(role1_slug)
        await self.db.select_role_permission_all()

        query1 = safe_insert_role_permission_by_slug(role1_uid, perm1_slug)
        await self.db.execute(query1)
        items1 = await self.db.select_role_permission_all()

        query2 = safe_insert_role_permission_by_slug(role1_slug, perm1_slug)
        await self.db.execute(query2)
        items2 = await self.db.select_role_permission_all()

        self.assertListEqual(items1, items2)

    async def test_insert_and_delete(self):
        perm1_uid = await self.db.insert_permission("test.perm1")
        role1_uid = await self.db.insert_role("role1")

        items1 = await self.db.select_role_permission_all()

        await self.db.insert_role_permission(role1_uid, perm1_uid)
        items2 = await self.db.select_role_permission_all()
        self.assertLessEqual(1, len(items2))
        self.assertEqual(len(items2), len(items1) + 1)

        await self.db.delete_role_permission(role1_uid, perm1_uid)
        items3 = await self.db.select_role_permission_all()
        self.assertEqual(len(items3), len(items1))


if __name__ == "__main__":
    main()
