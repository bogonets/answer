# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta
from tester import PostgresqlTestCase
from recc.variables.database import ANONYMOUS_GROUP_NAME, ANONYMOUS_GROUP_DESCRIPTION


class PgGroupTestCase(PostgresqlTestCase):
    async def test_anonymous_group(self):
        anonymous_group = await self.db.get_group_by_uid(self.anonymous_group_uid)
        self.assertEqual(ANONYMOUS_GROUP_NAME, anonymous_group.name)
        self.assertEqual(ANONYMOUS_GROUP_DESCRIPTION, anonymous_group.description)

    async def test_create_and_get(self):
        name1 = "group1"
        name2 = "group2"
        desc1 = "description1"
        desc2 = "description2"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        created_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.create_group(name1, desc1, created_at=created_at1)
        await self.db.create_group(name2, desc2, created_at=created_at2)
        group1 = await self.db.get_group_by_name(name1)
        group2 = await self.db.get_group_by_name(name2)
        self.assertEqual(name1, group1.name)
        self.assertEqual(name2, group2.name)
        self.assertEqual(desc1, group1.description)
        self.assertEqual(desc2, group2.description)
        self.assertEqual(created_at1, group1.created_at)
        self.assertEqual(created_at2, group2.created_at)
        self.assertIsNone(group1.extra)
        self.assertIsNone(group2.extra)
        self.assertIsNone(group1.updated_at)
        self.assertIsNone(group2.updated_at)

        group1_uid = group1.uid
        group2_uid = group2.uid
        self.assertNotEqual(group1_uid, group2_uid)

        group1_2nd = await self.db.get_group_by_uid(group1_uid)
        group2_2nd = await self.db.get_group_by_uid(group2_uid)
        self.assertEqual(group1, group1_2nd)
        self.assertEqual(group2, group2_2nd)

    async def test_update_description(self):
        name1 = "group1"
        name2 = "group2"
        await self.db.create_group(name1)
        await self.db.create_group(name2)
        group1_uid = (await self.db.get_group_by_name(name1)).uid

        desc1 = "description1"
        desc2 = "description2"
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_group_description_by_uid(group1_uid, desc1, updated_at1)
        await self.db.update_group_description_by_name(name2, desc2, updated_at2)

        group1 = await self.db.get_group_by_name(name1)
        group2 = await self.db.get_group_by_name(name2)
        self.assertEqual(desc1, group1.description)
        self.assertEqual(desc2, group2.description)
        self.assertEqual(updated_at1, group1.updated_at)
        self.assertEqual(updated_at2, group2.updated_at)

    async def test_update_extra(self):
        name1 = "group1"
        name2 = "group2"
        await self.db.create_group(name1)
        await self.db.create_group(name2)
        group1_uid = (await self.db.get_group_by_name(name1)).uid

        extra1 = {"a": 1, "b": 2}
        extra2 = {"c": 3, "d": 4}
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_group_extra_by_uid(group1_uid, extra1, updated_at1)
        await self.db.update_group_extra_by_name(name2, extra2, updated_at2)

        group1 = await self.db.get_group_by_name(name1)
        group2 = await self.db.get_group_by_name(name2)
        self.assertEqual(extra1, group1.extra)
        self.assertEqual(extra2, group2.extra)
        self.assertEqual(updated_at1, group1.updated_at)
        self.assertEqual(updated_at2, group2.updated_at)

    async def test_delete(self):
        name1 = "group1"
        name2 = "group2"
        await self.db.create_group(name1)
        await self.db.create_group(name2)
        group1_uid = (await self.db.get_group_by_name(name1)).uid
        group2_uid = (await self.db.get_group_by_name(name2)).uid

        groups1 = await self.db.get_groups()
        groups1_ids = [g.uid for g in groups1]
        self.assertEqual(3, len(groups1_ids))
        self.assertIn(self.anonymous_group_uid, groups1_ids)
        self.assertIn(group1_uid, groups1_ids)
        self.assertIn(group2_uid, groups1_ids)

        await self.db.delete_group_by_uid(group1_uid)
        await self.db.delete_group_by_name(name2)

        groups2 = await self.db.get_groups()
        groups2_ids = [g.uid for g in groups2]
        self.assertEqual(1, len(groups2_ids))
        self.assertIn(self.anonymous_group_uid, groups2_ids)


if __name__ == "__main__":
    unittest.main()
