# -*- coding: utf-8 -*-

from unittest import main
from recc.database.struct.group_join_member import GroupJoinGroupMember
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgGroupMemberTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()

        self.guest = await self.db.insert_rule("rule1")
        self.reporter = await self.db.insert_rule("rule2")
        self.operator = await self.db.insert_rule("rule3")
        self.maintainer = await self.db.insert_rule("rule4")

        self.user1_uid = await self.db.insert_user("user1", "pass1", "salt1")
        self.user2_uid = await self.db.insert_user("user2", "pass2", "salt2")

        self.group_uid = await self.db.insert_group("group")

    async def test_create_and_get(self):
        await self.db.insert_group_member(self.group_uid, self.user1_uid, self.guest)
        await self.db.insert_group_member(self.group_uid, self.user2_uid, self.reporter)

        member1 = await self.db.select_group_member(self.group_uid, self.user1_uid)
        member2 = await self.db.select_group_member(self.group_uid, self.user2_uid)

        self.assertEqual(self.group_uid, member1.group_uid)
        self.assertEqual(self.group_uid, member2.group_uid)
        self.assertEqual(self.user1_uid, member1.user_uid)
        self.assertEqual(self.user2_uid, member2.user_uid)
        self.assertEqual(self.guest, member1.rule_uid)
        self.assertEqual(self.reporter, member2.rule_uid)

    async def test_update_rule(self):
        await self.db.insert_group_member(self.group_uid, self.user1_uid, self.guest)
        await self.db.insert_group_member(self.group_uid, self.user2_uid, self.reporter)
        await self.db.update_group_member_rule(
            self.group_uid, self.user1_uid, self.maintainer
        )
        await self.db.update_group_member_rule(
            self.group_uid, self.user2_uid, self.operator
        )

        member1 = await self.db.select_group_member(self.group_uid, self.user1_uid)
        member2 = await self.db.select_group_member(self.group_uid, self.user2_uid)
        self.assertEqual(self.maintainer, member1.rule_uid)
        self.assertEqual(self.operator, member2.rule_uid)

    async def test_group_members(self):
        await self.db.insert_group_member(self.group_uid, self.user1_uid, self.guest)
        await self.db.insert_group_member(self.group_uid, self.user2_uid, self.reporter)

        groups1 = await self.db.select_group_members_by_group_uid(self.group_uid)
        groups2 = await self.db.select_group_members_by_user_uid(self.user2_uid)
        groups3 = await self.db.select_group_members()
        self.assertEqual(2, len(groups1))
        self.assertEqual(1, len(groups2))
        self.assertEqual(2, len(groups3))

    async def test_group_members_join_group(self):
        test_user = self.user1_uid
        fake_user = self.user2_uid

        await self.db.insert_group_member(self.group_uid, test_user, self.guest)
        await self.db.insert_group_member(self.group_uid, fake_user, self.reporter)

        groups = await self.db.select_group_members_join_group_by_user_uid(test_user)
        self.assertEqual(1, len(groups))
        group0 = groups[0]
        self.assertIsInstance(group0, GroupJoinGroupMember)
        self.assertEqual(self.group_uid, group0.group_uid)
        self.assertEqual(test_user, group0.user_uid)
        self.assertEqual(self.guest, group0.rule_uid)

        group1 = await self.db.select_group_member_join_group_by_user_uid_and_group_uid(
            test_user, self.group_uid
        )
        self.assertEqual(group0, group1)

    async def test_delete(self):
        await self.db.insert_group_member(self.group_uid, self.user1_uid, self.guest)
        await self.db.insert_group_member(self.group_uid, self.user2_uid, self.reporter)
        self.assertEqual(2, len(await self.db.select_group_members()))
        await self.db.delete_group_member(self.group_uid, self.user1_uid)
        await self.db.delete_group_member(self.group_uid, self.user2_uid)
        self.assertEqual(0, len(await self.db.select_group_members()))


if __name__ == "__main__":
    main()
