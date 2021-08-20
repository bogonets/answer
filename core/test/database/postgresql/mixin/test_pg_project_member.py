# -*- coding: utf-8 -*-

from unittest import main
from recc.database.struct.project_join_member import ProjectJoinMember
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgProjectMemberTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()

        self.project_slug = "project"
        await self.db.insert_project(self.anonymous_group_uid, self.project_slug)
        self.project_uid = await self.db.select_project_uid_by_group_uid_and_slug(
            self.anonymous_group_uid, self.project_slug
        )
        self.project = await self.db.select_project_by_uid(self.project_uid)

        self.guest = self.guest_permission_uid
        self.reporter = self.reporter_permission_uid
        self.operator = self.operator_permission_uid
        self.maintainer = self.maintainer_permission_uid

        user1_name = "user1"
        user2_name = "user2"
        await self.db.insert_user(user1_name, "pass1", "salt1")
        await self.db.insert_user(user2_name, "pass2", "salt2")

        user1_uid = await self.db.select_user_uid_by_username(user1_name)
        user2_uid = await self.db.select_user_uid_by_username(user2_name)
        self.user1 = await self.db.select_user_by_uid(user1_uid)
        self.user2 = await self.db.select_user_by_uid(user2_uid)

    async def test_create_and_get(self):
        await self.db.insert_project_member(
            self.project.uid, self.user1.uid, self.guest
        )
        await self.db.insert_project_member(
            self.project.uid, self.user2.uid, self.reporter
        )

        member1 = await self.db.select_project_member(self.project.uid, self.user1.uid)
        member2 = await self.db.select_project_member(self.project.uid, self.user2.uid)

        self.assertEqual(self.project.uid, member1.project_uid)
        self.assertEqual(self.project.uid, member2.project_uid)
        self.assertEqual(self.user1.uid, member1.user_uid)
        self.assertEqual(self.user2.uid, member2.user_uid)
        self.assertEqual(self.guest, member1.permission_uid)
        self.assertEqual(self.reporter, member2.permission_uid)

    async def test_update_permission(self):
        await self.db.insert_project_member(
            self.project.uid, self.user1.uid, self.guest
        )
        await self.db.insert_project_member(
            self.project.uid, self.user2.uid, self.reporter
        )
        await self.db.update_project_member_permission(
            self.project.uid, self.user1.uid, self.maintainer
        )
        await self.db.update_project_member_permission(
            self.project.uid, self.user2.uid, self.operator
        )

        member1 = await self.db.select_project_member(self.project.uid, self.user1.uid)
        member2 = await self.db.select_project_member(self.project.uid, self.user2.uid)
        self.assertEqual(self.maintainer, member1.permission_uid)
        self.assertEqual(self.operator, member2.permission_uid)

    async def test_project_members(self):
        await self.db.insert_project_member(
            self.project.uid, self.user1.uid, self.guest
        )
        await self.db.insert_project_member(
            self.project.uid, self.user2.uid, self.reporter
        )

        projects1 = await self.db.select_project_members_by_project_uid(
            self.project.uid
        )
        projects2 = await self.db.select_project_members_by_user_uid(self.user2.uid)
        projects3 = await self.db.select_project_members()
        self.assertEqual(2, len(projects1))
        self.assertEqual(1, len(projects2))
        self.assertEqual(2, len(projects3))

    async def test_group_members_join_group(self):
        test_user = self.user1.uid
        fake_user = self.user2.uid

        await self.db.insert_project_member(self.project.uid, test_user, self.guest)
        await self.db.insert_project_member(self.project.uid, fake_user, self.reporter)

        projects = await self.db.select_project_members_join_project_by_user_uid(
            test_user
        )
        self.assertEqual(1, len(projects))
        project0 = projects[0]
        self.assertIsInstance(project0, ProjectJoinMember)
        self.assertEqual(self.project.uid, project0.project_uid)
        self.assertEqual(test_user, project0.user_uid)
        self.assertEqual(self.guest, project0.permission_uid)

    async def test_delete(self):
        await self.db.insert_project_member(
            self.project.uid, self.user1.uid, self.guest
        )
        await self.db.insert_project_member(
            self.project.uid, self.user2.uid, self.reporter
        )
        self.assertEqual(2, len(await self.db.select_project_members()))
        await self.db.delete_project_member(self.project.uid, self.user1.uid)
        await self.db.delete_project_member(self.project.uid, self.user2.uid)
        self.assertEqual(0, len(await self.db.select_project_members()))


if __name__ == "__main__":
    main()
