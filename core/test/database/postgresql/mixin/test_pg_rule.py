# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from recc.variables.database import RULE_UID_OWNER, RULE_SLUG_OWNER


class PgRuleTestCase(PostgresqlTestCase):
    async def test_owner_rule(self):
        owner_uid = await self.db.select_rule_uid_by_slug(RULE_SLUG_OWNER)
        self.assertEqual(RULE_UID_OWNER, owner_uid)

    async def test_create_and_get(self):
        slug1 = "rule1"
        slug2 = "rule2"
        desc1 = "desc1"
        desc2 = "desc2"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        result1_uid = await self.db.insert_rule(
            slug1,
            description=desc1,
            w_graph=True,
            w_member=True,
            created_at=created_at1,
        )
        result2_uid = await self.db.insert_rule(
            slug2,
            description=desc2,
            r_layout=True,
            r_storage=True,
            created_at=created_at2,
        )
        rule1_uid = await self.db.select_rule_uid_by_slug(slug1)
        rule2_uid = await self.db.select_rule_uid_by_slug(slug2)
        self.assertEqual(result1_uid, rule1_uid)
        self.assertEqual(result2_uid, rule2_uid)
        rule1 = await self.db.select_rule_by_uid(rule1_uid)
        rule2 = await self.db.select_rule_by_uid(rule2_uid)
        self.assertEqual(slug1, rule1.slug)
        self.assertEqual(slug2, rule2.slug)
        self.assertIsNone(rule1.name)
        self.assertIsNone(rule2.name)
        self.assertEqual(desc1, rule1.description)
        self.assertEqual(desc2, rule2.description)
        self.assertEqual(created_at1, rule1.created_at)
        self.assertEqual(created_at2, rule2.created_at)

        self.assertFalse(rule1.r_layout)
        self.assertFalse(rule1.w_layout)
        self.assertFalse(rule1.r_storage)
        self.assertFalse(rule1.w_storage)
        self.assertFalse(rule1.r_manager)
        self.assertFalse(rule1.w_manager)
        self.assertFalse(rule1.r_graph)
        self.assertTrue(rule1.w_graph)
        self.assertFalse(rule1.r_member)
        self.assertTrue(rule1.w_member)
        self.assertFalse(rule1.r_setting)
        self.assertFalse(rule1.w_setting)
        self.assertFalse(rule1.hidden)
        self.assertFalse(rule1.lock)

        self.assertTrue(rule2.r_layout)
        self.assertFalse(rule2.w_layout)
        self.assertTrue(rule2.r_storage)
        self.assertFalse(rule2.w_storage)
        self.assertFalse(rule2.r_manager)
        self.assertFalse(rule2.w_manager)
        self.assertFalse(rule2.r_graph)
        self.assertFalse(rule2.w_graph)
        self.assertFalse(rule2.r_member)
        self.assertFalse(rule2.w_member)
        self.assertFalse(rule2.r_setting)
        self.assertFalse(rule2.w_setting)
        self.assertFalse(rule2.hidden)
        self.assertFalse(rule2.lock)

        self.assertIsNone(rule1.extra)
        self.assertIsNone(rule2.extra)
        self.assertIsNone(rule1.updated_at)
        self.assertIsNone(rule2.updated_at)

        rule1_uid = rule1.uid
        rule2_uid = rule2.uid
        self.assertNotEqual(rule1_uid, rule2_uid)

    async def test_update_rule(self):
        slug1 = "rule1"
        await self.db.insert_rule(slug1)
        rule1_uid = await self.db.select_rule_uid_by_slug(slug1)
        rule1 = await self.db.select_rule_by_uid(rule1_uid)
        self.assertEqual(slug1, rule1.slug)
        self.assertIsNone(rule1.name)
        self.assertIsNone(rule1.description)
        self.assertIsNone(rule1.extra)
        self.assertIsNone(rule1.updated_at)
        self.assertFalse(rule1.r_layout)
        self.assertFalse(rule1.w_layout)
        self.assertFalse(rule1.r_storage)
        self.assertFalse(rule1.w_storage)
        self.assertFalse(rule1.r_manager)
        self.assertFalse(rule1.w_manager)
        self.assertFalse(rule1.r_graph)
        self.assertFalse(rule1.w_graph)
        self.assertFalse(rule1.r_member)
        self.assertFalse(rule1.w_member)
        self.assertFalse(rule1.r_setting)
        self.assertFalse(rule1.w_setting)

        updated_slug = "rule2"
        updated_desc = "desc2"
        updated_extra = {"A": 65, "B": 66}
        updated_at = datetime.now().astimezone() + timedelta(days=7)
        await self.db.update_rule_by_uid(
            rule1.uid,
            slug=updated_slug,
            description=updated_desc,
            extra=updated_extra,
            r_layout=True,
            w_layout=True,
            w_graph=False,
            updated_at=updated_at,
        )
        updated_rule1 = await self.db.select_rule_by_uid(rule1.uid)
        self.assertEqual(updated_slug, updated_rule1.slug)
        self.assertIsNone(updated_rule1.name)
        self.assertEqual(updated_desc, updated_rule1.description)
        self.assertEqual(updated_extra, updated_rule1.extra)
        self.assertEqual(updated_at, updated_rule1.updated_at)
        self.assertTrue(updated_rule1.r_layout)
        self.assertTrue(updated_rule1.w_layout)
        self.assertFalse(updated_rule1.r_storage)
        self.assertFalse(updated_rule1.w_storage)
        self.assertFalse(updated_rule1.r_manager)
        self.assertFalse(updated_rule1.w_manager)
        self.assertFalse(updated_rule1.r_graph)
        self.assertFalse(updated_rule1.w_graph)
        self.assertFalse(updated_rule1.r_member)
        self.assertFalse(updated_rule1.w_member)
        self.assertFalse(updated_rule1.r_setting)
        self.assertFalse(updated_rule1.w_setting)
        self.assertFalse(updated_rule1.hidden)
        self.assertFalse(updated_rule1.lock)

    async def test_delete(self):
        rule1_uid = await self.db.insert_rule("rule1")

        rules1 = await self.db.select_rule_all()
        rules1_ids = [g.uid for g in rules1]
        self.assertIn(rule1_uid, rules1_ids)

        await self.db.delete_rule_by_uid(rule1_uid)

        rules2 = await self.db.select_rule_all()
        rules2_ids = [g.uid for g in rules2]
        self.assertNotIn(rule1_uid, rules2_ids)

    async def test_group_member_rule(self):
        rule1_uid = await self.db.insert_rule("rule1")

        user1_uid = await self.db.insert_user("user1", "pass", "salt")
        group1_uid = await self.db.insert_group("group1")
        await self.db.insert_group_member(group1_uid, user1_uid, rule1_uid)

        rule = await self.db.select_rule_by_user_uid_and_group_uid(
            user1_uid, group1_uid
        )
        self.assertEqual(rule1_uid, rule.uid)

    async def test_project_member_rule(self):
        rule1_uid = await self.db.insert_rule("rule1")
        rule2_uid = await self.db.insert_rule("rule2")

        user1_uid = await self.db.insert_user("user1", "pass", "salt")

        group1_uid = await self.db.insert_group("group1")
        await self.db.insert_group_member(group1_uid, user1_uid, rule1_uid)

        project1_uid = await self.db.insert_project(group1_uid, "project1")
        await self.db.insert_project_member(project1_uid, user1_uid, rule2_uid)

        rule = await self.db.select_rule_by_user_uid_and_project_uid(
            user1_uid, project1_uid
        )
        self.assertEqual(rule2_uid, rule.uid)

    async def test_project_rule(self):
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

        guest_uid = await self.db.insert_rule("rule1")
        reporter_uid = await self.db.insert_rule("rule2")
        operator_uid = await self.db.insert_rule("rule3")
        maintainer_uid = await self.db.insert_rule("rule4")

        # user1 // project1, project2, project3, project4
        # user2 // group1, group2
        # user3 // group1 < project1
        # user4 // group2 > project3
        # user5 // -
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

        u1p1 = await self.db.select_best_project_rule(user1_uid, project1_uid)
        u1p2 = await self.db.select_best_project_rule(user1_uid, project2_uid)
        u1p3 = await self.db.select_best_project_rule(user1_uid, project3_uid)
        u1p4 = await self.db.select_best_project_rule(user1_uid, project4_uid)
        u2p1 = await self.db.select_best_project_rule(user2_uid, project1_uid)
        u2p2 = await self.db.select_best_project_rule(user2_uid, project2_uid)
        u2p3 = await self.db.select_best_project_rule(user2_uid, project3_uid)
        u2p4 = await self.db.select_best_project_rule(user2_uid, project4_uid)
        u3p1 = await self.db.select_best_project_rule(user3_uid, project1_uid)
        u3p2 = await self.db.select_best_project_rule(user3_uid, project2_uid)
        u3p3 = await self.db.select_best_project_rule(user3_uid, project3_uid)
        u3p4 = await self.db.select_best_project_rule(user3_uid, project4_uid)
        u4p1 = await self.db.select_best_project_rule(user4_uid, project1_uid)
        u4p2 = await self.db.select_best_project_rule(user4_uid, project2_uid)
        u4p3 = await self.db.select_best_project_rule(user4_uid, project3_uid)
        u4p4 = await self.db.select_best_project_rule(user4_uid, project4_uid)
        u5p1 = await self.db.select_best_project_rule(user5_uid, project1_uid)
        u5p2 = await self.db.select_best_project_rule(user5_uid, project2_uid)
        u5p3 = await self.db.select_best_project_rule(user5_uid, project3_uid)
        u5p4 = await self.db.select_best_project_rule(user5_uid, project4_uid)

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
        slug1 = "rule1"
        features1 = ["a", "b"]
        await self.db.insert_rule(slug1, features=features1)
        uid1 = await self.db.select_rule_uid_by_slug(slug1)
        rule1 = await self.db.select_rule_by_uid(uid1)
        self.assertEqual(slug1, rule1.slug)
        self.assertEqual(features1, rule1.features)

        features2 = ["c", "d", "e"]
        await self.db.update_rule_by_uid(uid=uid1, features=features2)
        rule2 = await self.db.select_rule_by_uid(uid1)
        self.assertEqual(features2, rule2.features)

        features3 = ["f"]
        await self.db.update_rule_by_uid(uid=uid1, features=features3)
        rule3 = await self.db.select_rule_by_uid(uid1)
        self.assertEqual(features3, rule3.features)


if __name__ == "__main__":
    main()
