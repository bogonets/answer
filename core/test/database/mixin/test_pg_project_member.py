# -*- coding: utf-8 -*-

from unittest import main

from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgProjectMemberTestCase(PostgresqlTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.role1_uid = await self.db.insert_role("role1")
        self.role2_uid = await self.db.insert_role("role2")
        self.role3_uid = await self.db.insert_role("role3")
        self.role4_uid = await self.db.insert_role("role4")

        self.user1_uid = await self.db.insert_user("user1", "pass1", "salt1")
        self.user2_uid = await self.db.insert_user("user2", "pass2", "salt2")

        self.group_uid = await self.db.insert_group("group")
        self.project_uid = await self.db.insert_project(self.group_uid, "project")

    async def test_create_and_get(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.role1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.role2_uid
        )

        member1 = await self.db.select_project_member(self.project_uid, self.user1_uid)
        member2 = await self.db.select_project_member(self.project_uid, self.user2_uid)

        self.assertEqual(self.project_uid, member1.project_uid)
        self.assertEqual(self.project_uid, member2.project_uid)
        self.assertEqual(self.user1_uid, member1.user_uid)
        self.assertEqual(self.user2_uid, member2.user_uid)
        self.assertEqual(self.role1_uid, member1.role_uid)
        self.assertEqual(self.role2_uid, member2.role_uid)

    async def test_update_role(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.role1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.role2_uid
        )
        await self.db.update_project_member_role(
            self.project_uid, self.user1_uid, self.role4_uid
        )
        await self.db.update_project_member_role(
            self.project_uid, self.user2_uid, self.role3_uid
        )

        member1 = await self.db.select_project_member(self.project_uid, self.user1_uid)
        member2 = await self.db.select_project_member(self.project_uid, self.user2_uid)
        self.assertEqual(self.role4_uid, member1.role_uid)
        self.assertEqual(self.role3_uid, member2.role_uid)

    async def test_project_members(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.role1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.role2_uid
        )

        projects1 = await self.db.select_project_members_by_project_uid(
            self.project_uid
        )
        projects2 = await self.db.select_project_members_by_user_uid(self.user2_uid)
        projects3 = await self.db.select_project_members()
        self.assertEqual(2, len(projects1))
        self.assertEqual(1, len(projects2))
        self.assertEqual(2, len(projects3))

    async def test_delete(self):
        await self.db.insert_project_member(
            self.project_uid, self.user1_uid, self.role1_uid
        )
        await self.db.insert_project_member(
            self.project_uid, self.user2_uid, self.role2_uid
        )
        self.assertEqual(2, len(await self.db.select_project_members()))
        await self.db.delete_project_member(self.project_uid, self.user1_uid)
        await self.db.delete_project_member(self.project_uid, self.user2_uid)
        self.assertEqual(0, len(await self.db.select_project_members()))


if __name__ == "__main__":
    main()
