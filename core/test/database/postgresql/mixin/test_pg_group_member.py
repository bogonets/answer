# -*- coding: utf-8 -*-

import unittest
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgGroupMemberTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()

        self.guest = self.guest_permission_uid
        self.reporter = self.reporter_permission_uid
        self.operator = self.operator_permission_uid
        self.maintainer = self.maintainer_permission_uid
        self.anonymous = self.anonymous_group_uid

        user1_name = "user1"
        user2_name = "user2"
        await self.db.insert_user(user1_name, "pass1", "salt1")
        await self.db.insert_user(user2_name, "pass2", "salt2")

        self.user1_uid = await self.db.get_user_uid_by_username(user1_name)
        self.user2_uid = await self.db.get_user_uid_by_username(user2_name)

        self.user1 = await self.db.get_user_by_uid(self.user1_uid)
        self.user2 = await self.db.get_user_by_uid(self.user2_uid)

    async def test_create_and_get(self):
        await self.db.insert_group_member(self.anonymous, self.user1.uid, self.guest)
        await self.db.insert_group_member(self.anonymous, self.user2.uid, self.reporter)

        member1 = await self.db.get_group_member(self.anonymous, self.user1.uid)
        member2 = await self.db.get_group_member(self.anonymous, self.user2.uid)

        self.assertEqual(self.anonymous, member1.group_uid)
        self.assertEqual(self.anonymous, member2.group_uid)
        self.assertEqual(self.user1.uid, member1.user_uid)
        self.assertEqual(self.user2.uid, member2.user_uid)
        self.assertEqual(self.guest, member1.permission_uid)
        self.assertEqual(self.reporter, member2.permission_uid)

    async def test_update_permission(self):
        await self.db.insert_group_member(self.anonymous, self.user1.uid, self.guest)
        await self.db.insert_group_member(self.anonymous, self.user2.uid, self.reporter)
        await self.db.update_group_member_permission(
            self.anonymous, self.user1.uid, self.maintainer
        )
        await self.db.update_group_member_permission(
            self.anonymous, self.user2.uid, self.operator
        )

        member1 = await self.db.get_group_member(self.anonymous, self.user1.uid)
        member2 = await self.db.get_group_member(self.anonymous, self.user2.uid)
        self.assertEqual(self.maintainer, member1.permission_uid)
        self.assertEqual(self.operator, member2.permission_uid)

    async def test_group_members(self):
        await self.db.insert_group_member(self.anonymous, self.user1.uid, self.guest)
        await self.db.insert_group_member(self.anonymous, self.user2.uid, self.reporter)

        groups1 = await self.db.get_group_member_by_group_uid(self.anonymous)
        groups2 = await self.db.get_group_member_by_user_uid(self.user2.uid)
        groups3 = await self.db.get_group_members()
        self.assertEqual(2, len(groups1))
        self.assertEqual(1, len(groups2))
        self.assertEqual(2, len(groups3))

    async def test_delete(self):
        await self.db.insert_group_member(self.anonymous, self.user1.uid, self.guest)
        await self.db.insert_group_member(self.anonymous, self.user2.uid, self.reporter)
        self.assertEqual(2, len(await self.db.get_group_members()))
        await self.db.delete_group_member(self.anonymous, self.user1.uid)
        await self.db.delete_group_member(self.anonymous, self.user2.uid)
        self.assertEqual(0, len(await self.db.get_group_members()))


if __name__ == "__main__":
    unittest.main()
