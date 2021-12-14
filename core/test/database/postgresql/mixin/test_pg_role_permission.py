# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgRolePermissionTestCase(PostgresqlTestCase):
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
