# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from recc.variables.database import ANONYMOUS_GROUP_SLUG, ANONYMOUS_GROUP_DESCRIPTION


class PgGroupTestCase(PostgresqlTestCase):
    async def test_anonymous_group(self):
        anonymous_group = await self.db.get_group_by_uid(self.anonymous_group_uid)
        self.assertEqual(ANONYMOUS_GROUP_SLUG, anonymous_group.slug)
        self.assertEqual(ANONYMOUS_GROUP_DESCRIPTION, anonymous_group.description)

    async def test_create_and_get(self):
        slug1 = "slug1"
        slug2 = "slug2"
        name1 = "name1"
        name2 = "name2"
        desc1 = "description1"
        desc2 = "description2"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        created_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.create_group(slug1, name1, desc1, created_at=created_at1)
        await self.db.create_group(slug2, name2, desc2, created_at=created_at2)
        group1_uid = await self.db.get_group_uid_by_slug(slug1)
        group2_uid = await self.db.get_group_uid_by_slug(slug2)
        group1 = await self.db.get_group_by_uid(group1_uid)
        group2 = await self.db.get_group_by_uid(group2_uid)
        self.assertEqual(slug1, group1.slug)
        self.assertEqual(slug2, group2.slug)
        self.assertEqual(name1, group1.name)
        self.assertEqual(name2, group2.name)
        self.assertEqual(desc1, group1.description)
        self.assertEqual(desc2, group2.description)
        self.assertIsNone(group1.features)
        self.assertIsNone(group2.features)
        self.assertEqual(created_at1, group1.created_at)
        self.assertEqual(created_at2, group2.created_at)
        self.assertIsNone(group1.extra)
        self.assertIsNone(group2.extra)
        self.assertIsNone(group1.updated_at)
        self.assertIsNone(group2.updated_at)

        group1_uid = group1.uid
        group2_uid = group2.uid
        self.assertNotEqual(group1_uid, group2_uid)

        group1_uid_2nd = await self.db.get_group_uid_by_slug(group1.slug)
        self.assertEqual(group1.uid, group1_uid_2nd)
        group2_slug = await self.db.get_group_slug_by_uid(group2_uid)
        self.assertEqual(group2.slug, group2_slug)

    async def test_update(self):
        slug1 = "slug1"
        name1 = "name1"
        await self.db.create_group(slug1, name1)
        group1_uid = await self.db.get_group_uid_by_slug(slug1)

        desc1 = "description1"
        extra1 = {"a": 1, "b": 2}
        features1 = ["c", "d", "e"]
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        await self.db.update_group_by_uid(
            uid=group1_uid,
            description=desc1,
            extra=extra1,
            features=features1,
            updated_at=updated_at1,
        )

        group1 = await self.db.get_group_by_uid(group1_uid)
        self.assertEqual(desc1, group1.description)
        self.assertEqual(extra1, group1.extra)
        self.assertEqual(features1, group1.features)
        self.assertEqual(updated_at1, group1.updated_at)

    async def test_delete(self):
        slug1 = "group1"
        await self.db.create_group(slug1)
        group1_uid = await self.db.get_group_uid_by_slug(slug1)

        groups1 = await self.db.get_groups()
        groups1_ids = [g.uid for g in groups1]
        self.assertEqual(2, len(groups1_ids))
        self.assertIn(self.anonymous_group_uid, groups1_ids)
        self.assertIn(group1_uid, groups1_ids)

        await self.db.delete_group_by_uid(group1_uid)

        groups2 = await self.db.get_groups()
        groups2_ids = [g.uid for g in groups2]
        self.assertEqual(1, len(groups2_ids))
        self.assertIn(self.anonymous_group_uid, groups2_ids)


if __name__ == "__main__":
    main()
