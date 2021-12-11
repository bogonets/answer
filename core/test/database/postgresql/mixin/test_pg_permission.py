# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from recc.variables.database import RULE_UID_OWNER, RULE_SLUG_OWNER


class PgPermissionTestCase(PostgresqlTestCase):
    async def test_owner_permission(self):
        owner_uid = await self.db.select_permission_uid_by_slug(RULE_SLUG_OWNER)
        self.assertEqual(RULE_UID_OWNER, owner_uid)

    async def test_create_and_get(self):
        slug1 = "permission1"
        slug2 = "permission2"
        desc1 = "description1"
        desc2 = "description2"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        result1_uid = await self.db.insert_permission(
            slug1,
            description=desc1,
            w_graph=True,
            w_member=True,
            created_at=created_at1,
        )
        result2_uid = await self.db.insert_permission(
            slug2,
            description=desc2,
            r_layout=True,
            r_storage=True,
            created_at=created_at2,
        )
        permission1_uid = await self.db.select_permission_uid_by_slug(slug1)
        permission2_uid = await self.db.select_permission_uid_by_slug(slug2)
        self.assertEqual(result1_uid, permission1_uid)
        self.assertEqual(result2_uid, permission2_uid)
        permission1 = await self.db.select_permission_by_uid(permission1_uid)
        permission2 = await self.db.select_permission_by_uid(permission2_uid)
        self.assertEqual(slug1, permission1.slug)
        self.assertEqual(slug2, permission2.slug)
        self.assertIsNone(permission1.name)
        self.assertIsNone(permission2.name)
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
        self.assertFalse(permission1.hidden)
        self.assertFalse(permission1.lock)

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
        self.assertFalse(permission2.hidden)
        self.assertFalse(permission2.lock)

        self.assertIsNone(permission1.extra)
        self.assertIsNone(permission2.extra)
        self.assertIsNone(permission1.updated_at)
        self.assertIsNone(permission2.updated_at)

        permission1_uid = permission1.uid
        permission2_uid = permission2.uid
        self.assertNotEqual(permission1_uid, permission2_uid)

    async def test_update_permission(self):
        slug1 = "permission1"
        await self.db.insert_permission(slug1)
        permission1_uid = await self.db.select_permission_uid_by_slug(slug1)
        permission1 = await self.db.select_permission_by_uid(permission1_uid)
        self.assertEqual(slug1, permission1.slug)
        self.assertIsNone(permission1.name)
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

        updated_slug = "Unknown"
        updated_desc = "Test Permission"
        updated_extra = {"A": 65, "B": 66}
        updated_at = datetime.now().astimezone() + timedelta(days=7)
        await self.db.update_permission_by_uid(
            permission1.uid,
            slug=updated_slug,
            description=updated_desc,
            extra=updated_extra,
            r_layout=True,
            w_layout=True,
            w_graph=False,
            updated_at=updated_at,
        )
        updated_permission1 = await self.db.select_permission_by_uid(permission1.uid)
        self.assertEqual(updated_slug, updated_permission1.slug)
        self.assertIsNone(updated_permission1.name)
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
        self.assertFalse(updated_permission1.hidden)
        self.assertFalse(updated_permission1.lock)

    async def test_delete(self):
        perm1_uid = await self.db.insert_permission("perm1")

        perms1 = await self.db.select_permissions()
        perms1_ids = [g.uid for g in perms1]
        self.assertIn(perm1_uid, perms1_ids)

        await self.db.delete_permission_by_uid(perm1_uid)

        perms2 = await self.db.select_permissions()
        perms2_ids = [g.uid for g in perms2]
        self.assertNotIn(perm1_uid, perms2_ids)

    async def test_group_member_permission(self):
        parm1_uid = await self.db.insert_permission("perm1")

        user1_uid = await self.db.insert_user("user1", "pass", "salt")
        group1_uid = await self.db.insert_group("group1")
        await self.db.insert_group_member(group1_uid, user1_uid, parm1_uid)

        permission = await self.db.select_permission_by_user_uid_and_group_uid(
            user1_uid, group1_uid
        )
        self.assertEqual(parm1_uid, permission.uid)

    async def test_project_member_permission(self):
        perm1_uid = await self.db.insert_permission("perm1")
        perm2_uid = await self.db.insert_permission("perm2")

        user1_uid = await self.db.insert_user("user1", "pass", "salt")

        group1_uid = await self.db.insert_group("group1")
        await self.db.insert_group_member(group1_uid, user1_uid, perm1_uid)

        project1_uid = await self.db.insert_project(group1_uid, "project1")
        await self.db.insert_project_member(project1_uid, user1_uid, perm2_uid)

        permission = await self.db.select_permission_by_user_uid_and_project_uid(
            user1_uid, project1_uid
        )
        self.assertEqual(perm2_uid, permission.uid)

    async def test_project_permission(self):
        user1_uid = await self.db.insert_user("user1", "pass", "salt")
        user2_uid = await self.db.insert_user("user2", "pass", "salt")
        user3_uid = await self.db.insert_user("user3", "pass", "salt")
        user4_uid = await self.db.insert_user("user4", "pass", "salt")
        user5_uid = await self.db.insert_user("user5", "pass", "salt")

        group1_uid = await self.db.insert_group("group1")
        group2_uid = await self.db.insert_group("group2")

        project1_uid = await self.db.insert_project(group1_uid, "project1")
        project2_uid = await self.db.insert_project(group1_uid, "project2")
        project3_uid = await self.db.insert_project(group2_uid, "project3")
        project4_uid = await self.db.insert_project(group2_uid, "project4")

        guest_uid = await self.db.insert_permission("perm1")
        reporter_uid = await self.db.insert_permission("perm2")
        operator_uid = await self.db.insert_permission("perm3")
        maintainer_uid = await self.db.insert_permission("perm4")

        # user1 -> project1, project2, project3, project4
        # user2 -> group1, group2
        # user3 -> group1 < project1
        # user4 -> group2 > project3
        # user5 -> -
        await self.db.insert_project_member(project1_uid, user1_uid, guest_uid)
        await self.db.insert_project_member(project2_uid, user1_uid, guest_uid)
        await self.db.insert_project_member(project3_uid, user1_uid, guest_uid)
        await self.db.insert_project_member(project4_uid, user1_uid, guest_uid)

        await self.db.insert_group_member(group1_uid, user2_uid, reporter_uid)
        await self.db.insert_group_member(group2_uid, user2_uid, reporter_uid)

        await self.db.insert_group_member(group1_uid, user3_uid, guest_uid)
        await self.db.insert_project_member(project1_uid, user3_uid, operator_uid)

        await self.db.insert_group_member(group2_uid, user4_uid, maintainer_uid)
        await self.db.insert_project_member(project3_uid, user4_uid, guest_uid)

        u1p1 = await self.db.select_best_project_permission(user1_uid, project1_uid)
        u1p2 = await self.db.select_best_project_permission(user1_uid, project2_uid)
        u1p3 = await self.db.select_best_project_permission(user1_uid, project3_uid)
        u1p4 = await self.db.select_best_project_permission(user1_uid, project4_uid)
        u2p1 = await self.db.select_best_project_permission(user2_uid, project1_uid)
        u2p2 = await self.db.select_best_project_permission(user2_uid, project2_uid)
        u2p3 = await self.db.select_best_project_permission(user2_uid, project3_uid)
        u2p4 = await self.db.select_best_project_permission(user2_uid, project4_uid)
        u3p1 = await self.db.select_best_project_permission(user3_uid, project1_uid)
        u3p2 = await self.db.select_best_project_permission(user3_uid, project2_uid)
        u3p3 = await self.db.select_best_project_permission(user3_uid, project3_uid)
        u3p4 = await self.db.select_best_project_permission(user3_uid, project4_uid)
        u4p1 = await self.db.select_best_project_permission(user4_uid, project1_uid)
        u4p2 = await self.db.select_best_project_permission(user4_uid, project2_uid)
        u4p3 = await self.db.select_best_project_permission(user4_uid, project3_uid)
        u4p4 = await self.db.select_best_project_permission(user4_uid, project4_uid)
        u5p1 = await self.db.select_best_project_permission(user5_uid, project1_uid)
        u5p2 = await self.db.select_best_project_permission(user5_uid, project2_uid)
        u5p3 = await self.db.select_best_project_permission(user5_uid, project3_uid)
        u5p4 = await self.db.select_best_project_permission(user5_uid, project4_uid)

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

    async def test_features(self):
        slug1 = "slug1"
        features1 = ["a", "b"]
        await self.db.insert_permission(slug1, features=features1)
        uid1 = await self.db.select_permission_uid_by_slug(slug1)
        perm1 = await self.db.select_permission_by_uid(uid1)
        self.assertEqual(slug1, perm1.slug)
        self.assertEqual(features1, perm1.features)

        features2 = ["c", "d", "e"]
        await self.db.update_permission_by_uid(uid=uid1, features=features2)
        perm2 = await self.db.select_permission_by_uid(uid1)
        self.assertEqual(features2, perm2.features)

        features3 = ["f"]
        await self.db.update_permission_by_uid(uid=uid1, features=features3)
        perm3 = await self.db.select_permission_by_uid(uid1)
        self.assertEqual(features3, perm3.features)


if __name__ == "__main__":
    main()
