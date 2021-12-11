# -*- coding: utf-8 -*-

from unittest import main
from recc.database.struct.project_join_member import ProjectJoinProjectMember
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgProjectMemberTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()

        self.rule1_uid = await self.db.insert_rule("rule1")
        self.rule2_uid = await self.db.insert_rule("rule2")
        self.rule3_uid = await self.db.insert_rule("rule3")
        self.rule4_uid = await self.db.insert_rule("rule4")

        self.user1_uid = await self.db.insert_user("user1", "pass1", "salt1")
        self.user2_uid = await self.db.insert_user("user2", "pass2", "salt2")

        self.group_uid = await self.db.insert_group("group")
        self.project_uid = await self.db.insert_project(self.group_uid, "project")

    async def test_create_and_get(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.rule1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.rule2_uid
        )

        member1 = await self.db.select_project_member(self.project_uid, self.user1_uid)
        member2 = await self.db.select_project_member(self.project_uid, self.user2_uid)

        self.assertEqual(self.project_uid, member1.project_uid)
        self.assertEqual(self.project_uid, member2.project_uid)
        self.assertEqual(self.user1_uid, member1.user_uid)
        self.assertEqual(self.user2_uid, member2.user_uid)
        self.assertEqual(self.rule1_uid, member1.permission_uid)
        self.assertEqual(self.rule2_uid, member2.permission_uid)

    async def test_update_permission(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.rule1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.rule2_uid
        )
        await self.db.update_project_member_permission(
            self.project_uid, self.user1_uid, self.rule4_uid
        )
        await self.db.update_project_member_permission(
            self.project_uid, self.user2_uid, self.rule3_uid
        )

        member1 = await self.db.select_project_member(self.project_uid, self.user1_uid)
        member2 = await self.db.select_project_member(self.project_uid, self.user2_uid)
        self.assertEqual(self.rule4_uid, member1.permission_uid)
        self.assertEqual(self.rule3_uid, member2.permission_uid)

    async def test_project_members(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.rule1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.rule2_uid
        )

        projects1 = await self.db.select_project_members_by_project_uid(
            self.project_uid
        )
        projects2 = await self.db.select_project_members_by_user_uid(self.user2_uid)
        projects3 = await self.db.select_project_members()
        self.assertEqual(2, len(projects1))
        self.assertEqual(1, len(projects2))
        self.assertEqual(2, len(projects3))

    async def test_group_members_join_group(self):
        test_user = self.user1_uid
        fake_user = self.user2_uid

        await self.db.insert_project_member(self.project_uid, test_user, self.rule1_uid)
        await self.db.insert_project_member(self.project_uid, fake_user, self.rule2_uid)

        projects = await self.db.select_project_members_join_project_by_user_uid(
            test_user
        )
        self.assertEqual(1, len(projects))
        project0 = projects[0]
        self.assertIsInstance(project0, ProjectJoinProjectMember)
        self.assertEqual(self.project_uid, project0.project_uid)
        self.assertEqual(test_user, project0.user_uid)
        self.assertEqual(self.rule1_uid, project0.permission_uid)

        project1 = await self.db.select_project_member_join_project_by_user_uid_and_project_uid(  # noqa
            test_user, self.project_uid
        )
        self.assertEqual(project0, project1)

    async def test_delete(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.rule1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.rule2_uid
        )
        self.assertEqual(2, len(await self.db.select_project_members()))
        await self.db.delete_project_member(self.project_uid, self.user1_uid)
        await self.db.delete_project_member(self.project_uid, self.user2_uid)
        self.assertEqual(0, len(await self.db.select_project_members()))


if __name__ == "__main__":
    main()
