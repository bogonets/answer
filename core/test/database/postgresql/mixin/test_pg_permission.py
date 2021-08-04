# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgPermissionTestCase(PostgresqlTestCase):
    async def test_create_and_get(self):
        name1 = "permission1"
        name2 = "permission2"
        desc1 = "description1"
        desc2 = "description2"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        created_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.create_permission(
            name1, desc1, w_graph=True, w_member=True, created_at=created_at1
        )
        await self.db.create_permission(
            name2, desc2, r_layout=True, r_storage=True, created_at=created_at2
        )
        permission1 = await self.db.get_permission_by_name(name1)
        permission2 = await self.db.get_permission_by_name(name2)
        self.assertEqual(name1, permission1.name)
        self.assertEqual(name2, permission2.name)
        self.assertEqual(desc1, permission1.description)
        self.assertEqual(desc2, permission2.description)
        self.assertEqual(created_at1, permission1.created_at)
        self.assertEqual(created_at2, permission2.created_at)

        self.assertFalse(permission1.r_layout)
        self.assertFalse(permission1.w_layout)
        self.assertFalse(permission1.r_storage)
        self.assertFalse(permission1.w_storage)
        self.assertFalse(permission1.r_manager)
        self.assertFalse(permission1.w_manager)
        self.assertFalse(permission1.r_graph)
        self.assertTrue(permission1.w_graph)
        self.assertFalse(permission1.r_member)
        self.assertTrue(permission1.w_member)
        self.assertFalse(permission1.r_setting)
        self.assertFalse(permission1.w_setting)

        self.assertTrue(permission2.r_layout)
        self.assertFalse(permission2.w_layout)
        self.assertTrue(permission2.r_storage)
        self.assertFalse(permission2.w_storage)
        self.assertFalse(permission2.r_manager)
        self.assertFalse(permission2.w_manager)
        self.assertFalse(permission2.r_graph)
        self.assertFalse(permission2.w_graph)
        self.assertFalse(permission2.r_member)
        self.assertFalse(permission2.w_member)
        self.assertFalse(permission2.r_setting)
        self.assertFalse(permission2.w_setting)

        self.assertIsNone(permission1.extra)
        self.assertIsNone(permission2.extra)
        self.assertIsNone(permission1.updated_at)
        self.assertIsNone(permission2.updated_at)

        permission1_uid = permission1.uid
        permission2_uid = permission2.uid
        self.assertNotEqual(permission1_uid, permission2_uid)

        permission1_2nd = await self.db.get_permission_by_uid(permission1_uid)
        permission2_2nd = await self.db.get_permission_by_uid(permission2_uid)
        self.assertEqual(permission1, permission1_2nd)
        self.assertEqual(permission2, permission2_2nd)

    async def test_update_description(self):
        name1 = "permission1"
        name2 = "permission2"
        await self.db.create_permission(name1)
        await self.db.create_permission(name2)
        permission1_uid = (await self.db.get_permission_by_name(name1)).uid

        desc1 = "description1"
        desc2 = "description2"
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_permission_description_by_uid(
            permission1_uid, desc1, updated_at1
        )
        await self.db.update_permission_description_by_name(name2, desc2, updated_at2)

        permission1 = await self.db.get_permission_by_name(name1)
        permission2 = await self.db.get_permission_by_name(name2)
        self.assertEqual(desc1, permission1.description)
        self.assertEqual(desc2, permission2.description)
        self.assertEqual(updated_at1, permission1.updated_at)
        self.assertEqual(updated_at2, permission2.updated_at)

    async def test_update_extra(self):
        name1 = "permission1"
        name2 = "permission2"
        await self.db.create_permission(name1)
        await self.db.create_permission(name2)
        permission1_uid = (await self.db.get_permission_by_name(name1)).uid

        extra1 = {"a": 1, "b": 2}
        extra2 = {"c": 3, "d": 4}
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_permission_extra_by_uid(
            permission1_uid, extra1, updated_at1
        )
        await self.db.update_permission_extra_by_name(name2, extra2, updated_at2)

        permission1 = await self.db.get_permission_by_name(name1)
        permission2 = await self.db.get_permission_by_name(name2)
        self.assertEqual(extra1, permission1.extra)
        self.assertEqual(extra2, permission2.extra)
        self.assertEqual(updated_at1, permission1.updated_at)
        self.assertEqual(updated_at2, permission2.updated_at)

    async def test_update_permission(self):
        name1 = "permission1"
        await self.db.create_permission(name1)
        permission1 = await self.db.get_permission_by_name(name1)
        self.assertEqual(name1, permission1.name)
        self.assertIsNone(permission1.description)
        self.assertIsNone(permission1.extra)
        self.assertIsNone(permission1.updated_at)
        self.assertFalse(permission1.r_layout)
        self.assertFalse(permission1.w_layout)
        self.assertFalse(permission1.r_storage)
        self.assertFalse(permission1.w_storage)
        self.assertFalse(permission1.r_manager)
        self.assertFalse(permission1.w_manager)
        self.assertFalse(permission1.r_graph)
        self.assertFalse(permission1.w_graph)
        self.assertFalse(permission1.r_member)
        self.assertFalse(permission1.w_member)
        self.assertFalse(permission1.r_setting)
        self.assertFalse(permission1.w_setting)

        updated_name = "Unknown"
        updated_desc = "Test Permission"
        updated_extra = {"A": 65, "B": 66}
        updated_at = datetime.utcnow() + timedelta(days=7)
        await self.db.update_permission_by_uid(
            permission1.uid,
            name=updated_name,
            description=updated_desc,
            extra=updated_extra,
            r_layout=True,
            w_layout=True,
            w_graph=False,
            updated_at=updated_at,
        )
        updated_permission1 = await self.db.get_permission_by_uid(permission1.uid)
        self.assertEqual(updated_name, updated_permission1.name)
        self.assertEqual(updated_desc, updated_permission1.description)
        self.assertEqual(updated_extra, updated_permission1.extra)
        self.assertEqual(updated_at, updated_permission1.updated_at)
        self.assertTrue(updated_permission1.r_layout)
        self.assertTrue(updated_permission1.w_layout)
        self.assertFalse(updated_permission1.r_storage)
        self.assertFalse(updated_permission1.w_storage)
        self.assertFalse(updated_permission1.r_manager)
        self.assertFalse(updated_permission1.w_manager)
        self.assertFalse(updated_permission1.r_graph)
        self.assertFalse(updated_permission1.w_graph)
        self.assertFalse(updated_permission1.r_member)
        self.assertFalse(updated_permission1.w_member)
        self.assertFalse(updated_permission1.r_setting)
        self.assertFalse(updated_permission1.w_setting)

    async def test_delete(self):
        name1 = "permission1"
        name2 = "permission2"
        await self.db.create_permission(name1)
        await self.db.create_permission(name2)
        permission1_uid = (await self.db.get_permission_by_name(name1)).uid
        permission2_uid = (await self.db.get_permission_by_name(name2)).uid

        permissions1 = await self.db.get_permissions()
        permissions1_ids = [g.uid for g in permissions1]
        self.assertEqual(6, len(permissions1_ids))
        self.assertIn(self.guest_permission_uid, permissions1_ids)
        self.assertIn(self.reporter_permission_uid, permissions1_ids)
        self.assertIn(self.operator_permission_uid, permissions1_ids)
        self.assertIn(self.maintainer_permission_uid, permissions1_ids)
        self.assertIn(permission1_uid, permissions1_ids)
        self.assertIn(permission2_uid, permissions1_ids)

        await self.db.delete_permission_by_uid(permission1_uid)
        await self.db.delete_permission_by_name(name2)

        permissions2 = await self.db.get_permissions()
        permissions2_ids = [g.uid for g in permissions2]
        self.assertEqual(4, len(permissions2_ids))
        self.assertIn(self.guest_permission_uid, permissions2_ids)
        self.assertIn(self.reporter_permission_uid, permissions2_ids)
        self.assertIn(self.operator_permission_uid, permissions2_ids)
        self.assertIn(self.maintainer_permission_uid, permissions2_ids)

    async def test_project_permission(self):
        user1_name = "user1"
        user2_name = "user2"
        user3_name = "user3"
        user4_name = "user4"
        user5_name = "user5"
        await self.db.create_user(user1_name, "pass", "salt")
        await self.db.create_user(user2_name, "pass", "salt")
        await self.db.create_user(user3_name, "pass", "salt")
        await self.db.create_user(user4_name, "pass", "salt")
        await self.db.create_user(user5_name, "pass", "salt")
        user1 = await self.db.get_user_by_username(user1_name)
        user2 = await self.db.get_user_by_username(user2_name)
        user3 = await self.db.get_user_by_username(user3_name)
        user4 = await self.db.get_user_by_username(user4_name)
        user5 = await self.db.get_user_by_username(user5_name)

        group1_name = "group1"
        group2_name = "group2"
        await self.db.create_group(group1_name)
        await self.db.create_group(group2_name)
        group1 = await self.db.get_group_by_name(group1_name)
        group2 = await self.db.get_group_by_name(group2_name)

        project1_name = "project1"
        project2_name = "project2"
        project3_name = "project3"
        project4_name = "project4"
        await self.db.create_project(group1.uid, project1_name)
        await self.db.create_project(group1.uid, project2_name)
        await self.db.create_project(group2.uid, project3_name)
        await self.db.create_project(group2.uid, project4_name)
        project1 = await self.db.get_project_by_name(group1.uid, project1_name)
        project2 = await self.db.get_project_by_name(group1.uid, project2_name)
        project3 = await self.db.get_project_by_name(group2.uid, project3_name)
        project4 = await self.db.get_project_by_name(group2.uid, project4_name)

        guest_uid = self.guest_permission_uid
        reporter_uid = self.reporter_permission_uid
        operator_uid = self.operator_permission_uid
        maintainer_uid = self.maintainer_permission_uid

        # user1 -> project1, project2, project3, project4
        # user2 -> group1, group2
        # user3 -> group1 < project1
        # user4 -> group2 > project3
        # user5 -> -
        await self.db.create_project_member(project1.uid, user1.uid, guest_uid)
        await self.db.create_project_member(project2.uid, user1.uid, guest_uid)
        await self.db.create_project_member(project3.uid, user1.uid, guest_uid)
        await self.db.create_project_member(project4.uid, user1.uid, guest_uid)

        await self.db.create_group_member(group1.uid, user2.uid, reporter_uid)
        await self.db.create_group_member(group2.uid, user2.uid, reporter_uid)

        await self.db.create_group_member(group1.uid, user3.uid, guest_uid)
        await self.db.create_project_member(project1.uid, user3.uid, operator_uid)

        await self.db.create_group_member(group2.uid, user4.uid, maintainer_uid)
        await self.db.create_project_member(project3.uid, user4.uid, guest_uid)

        u1p1 = await self.db.get_project_permission_by_uid(user1.uid, project1.uid)
        u1p2 = await self.db.get_project_permission_by_uid(user1.uid, project2.uid)
        u1p3 = await self.db.get_project_permission_by_uid(user1.uid, project3.uid)
        u1p4 = await self.db.get_project_permission_by_uid(user1.uid, project4.uid)
        u2p1 = await self.db.get_project_permission_by_uid(user2.uid, project1.uid)
        u2p2 = await self.db.get_project_permission_by_uid(user2.uid, project2.uid)
        u2p3 = await self.db.get_project_permission_by_uid(user2.uid, project3.uid)
        u2p4 = await self.db.get_project_permission_by_uid(user2.uid, project4.uid)
        u3p1 = await self.db.get_project_permission_by_uid(user3.uid, project1.uid)
        u3p2 = await self.db.get_project_permission_by_uid(user3.uid, project2.uid)
        u3p3 = await self.db.get_project_permission_by_uid(user3.uid, project3.uid)
        u3p4 = await self.db.get_project_permission_by_uid(user3.uid, project4.uid)
        u4p1 = await self.db.get_project_permission_by_uid(user4.uid, project1.uid)
        u4p2 = await self.db.get_project_permission_by_uid(user4.uid, project2.uid)
        u4p3 = await self.db.get_project_permission_by_uid(user4.uid, project3.uid)
        u4p4 = await self.db.get_project_permission_by_uid(user4.uid, project4.uid)
        u5p1 = await self.db.get_project_permission_by_uid(user5.uid, project1.uid)
        u5p2 = await self.db.get_project_permission_by_uid(user5.uid, project2.uid)
        u5p3 = await self.db.get_project_permission_by_uid(user5.uid, project3.uid)
        u5p4 = await self.db.get_project_permission_by_uid(user5.uid, project4.uid)

        self.assertEqual(guest_uid, u1p1.uid)
        self.assertEqual(guest_uid, u1p2.uid)
        self.assertEqual(guest_uid, u1p3.uid)
        self.assertEqual(guest_uid, u1p4.uid)
        self.assertEqual(reporter_uid, u2p1.uid)
        self.assertEqual(reporter_uid, u2p2.uid)
        self.assertEqual(reporter_uid, u2p3.uid)
        self.assertEqual(reporter_uid, u2p4.uid)
        self.assertEqual(operator_uid, u3p1.uid)
        self.assertEqual(guest_uid, u3p2.uid)
        self.assertIsNone(u3p3.uid)
        self.assertIsNone(u3p4.uid)
        self.assertIsNone(u4p1.uid)
        self.assertIsNone(u4p2.uid)
        self.assertEqual(guest_uid, u4p3.uid)
        self.assertEqual(maintainer_uid, u4p4.uid)
        self.assertIsNone(u5p1.uid)
        self.assertIsNone(u5p2.uid)
        self.assertIsNone(u5p3.uid)
        self.assertIsNone(u5p4.uid)


if __name__ == "__main__":
    unittest.main()