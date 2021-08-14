# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgProjectTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()
        self.group = await self.db.get_group_by_uid(self.anonymous_group_uid)

    async def test_none_exists_get(self):
        group_uid = self.group.uid
        group_slug = self.group.slug
        slug = "project"
        unknown = "unknown"
        await self.db.create_project(group_uid, slug)

        with self.assertRaises(RuntimeError):
            await self.db.get_project_by_fullpath(unknown, slug)
        with self.assertRaises(RuntimeError):
            await self.db.get_project_by_fullpath(group_slug, unknown)

        with self.assertRaises(RuntimeError):
            await self.db.get_project_uid_by_fullpath(unknown, slug)
        with self.assertRaises(RuntimeError):
            await self.db.get_project_uid_by_fullpath(group_slug, unknown)

    async def test_create_and_get(self):
        slug1 = "slug1"
        slug2 = "slug2"
        name1 = "name1"
        name2 = "name2"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        created_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.create_project(
            self.group.uid, slug1, name1, created_at=created_at1
        )
        await self.db.create_project(
            self.group.uid, slug2, name2, created_at=created_at2
        )
        project1 = await self.db.get_project_by_slug(self.group.uid, slug1)
        project2 = await self.db.get_project_by_slug(self.group.uid, slug2)

        self.assertEqual(self.group.uid, project1.group_uid)
        self.assertEqual(self.group.uid, project2.group_uid)
        self.assertEqual(slug1, project1.slug)
        self.assertEqual(slug2, project2.slug)
        self.assertEqual(name1, project1.name)
        self.assertEqual(name2, project2.name)
        self.assertIsNone(project1.description)
        self.assertIsNone(project2.description)
        self.assertIsNone(project1.features)
        self.assertIsNone(project2.features)
        self.assertIsNone(project1.extra)
        self.assertIsNone(project2.extra)
        self.assertEqual(created_at1, project1.created_at)
        self.assertEqual(created_at2, project2.created_at)
        self.assertIsNone(project1.updated_at)
        self.assertIsNone(project2.updated_at)

        project1_2nd = await self.db.get_project_by_uid(project1.uid)
        project2_2nd = await self.db.get_project_by_uid(project2.uid)
        self.assertEqual(project1, project1_2nd)
        self.assertEqual(project2, project2_2nd)

        group_slug = self.group.slug
        project1_3rd = await self.db.get_project_by_fullpath(group_slug, slug1)
        project2_3rd = await self.db.get_project_by_fullpath(group_slug, slug2)
        self.assertEqual(project1, project1_3rd)
        self.assertEqual(project2, project2_3rd)

        project1_4th_uid = await self.db.get_project_uid_by_fullpath(group_slug, slug1)
        project2_4th_uid = await self.db.get_project_uid_by_fullpath(group_slug, slug2)
        self.assertEqual(project1.uid, project1_4th_uid)
        self.assertEqual(project2.uid, project2_4th_uid)

    async def test_update_description(self):
        slug1 = "project1"
        slug2 = "project2"
        await self.db.create_project(self.group.uid, slug1)
        await self.db.create_project(self.group.uid, slug2)
        project1_uid = (await self.db.get_project_by_slug(self.group.uid, slug1)).uid

        desc1 = "description1"
        desc2 = "description2"
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_project_description_by_uid(
            project1_uid, desc1, updated_at1
        )
        await self.db.update_project_description_by_slug(
            self.group.uid, slug2, desc2, updated_at2
        )

        project1 = await self.db.get_project_by_slug(self.group.uid, slug1)
        project2 = await self.db.get_project_by_slug(self.group.uid, slug2)
        self.assertEqual(desc1, project1.description)
        self.assertEqual(desc2, project2.description)
        self.assertEqual(updated_at1, project1.updated_at)
        self.assertEqual(updated_at2, project2.updated_at)

    async def test_update_extra(self):
        slug1 = "project1"
        slug2 = "project2"
        await self.db.create_project(self.group.uid, slug1)
        await self.db.create_project(self.group.uid, slug2)
        project1_uid = (await self.db.get_project_by_slug(self.group.uid, slug1)).uid

        extra1 = {"a": 1, "b": 2}
        extra2 = {"c": 3, "d": 4}
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_project_extra_by_uid(project1_uid, extra1, updated_at1)
        await self.db.update_project_extra_by_slug(
            self.group.uid, slug2, extra2, updated_at2
        )

        project1 = await self.db.get_project_by_slug(self.group.uid, slug1)
        project2 = await self.db.get_project_by_slug(self.group.uid, slug2)
        self.assertEqual(extra1, project1.extra)
        self.assertEqual(extra2, project2.extra)
        self.assertEqual(updated_at1, project1.updated_at)
        self.assertEqual(updated_at2, project2.updated_at)

    async def test_delete(self):
        slug1 = "project1"
        slug2 = "project2"
        await self.db.create_project(self.group.uid, slug1)
        await self.db.create_project(self.group.uid, slug2)
        project1_uid = (await self.db.get_project_by_slug(self.group.uid, slug1)).uid

        projects1 = await self.db.get_project_by_group_uid(self.group.uid)
        self.assertEqual(2, len(projects1))

        await self.db.delete_project_by_uid(project1_uid)
        await self.db.delete_project_by_slug(self.group.uid, slug2)

        projects2 = await self.db.get_project_by_group_uid(self.group.uid)
        self.assertEqual(0, len(projects2))

    async def test_features(self):
        slug1 = "project1"
        features1 = ["a", "b"]
        await self.db.create_project(self.group.uid, slug1, features=features1)
        project1 = await self.db.get_project_by_slug(self.group.uid, slug1)

        self.assertEqual(self.group.uid, project1.group_uid)
        self.assertEqual(slug1, project1.slug)
        self.assertEqual(features1, project1.features)

        features2 = ["c", "d", "e"]
        await self.db.update_project_features_by_uid(project1.uid, features2)
        project2 = await self.db.get_project_by_slug(self.group.uid, slug1)
        self.assertEqual(features2, project2.features)

        features3 = ["f"]
        await self.db.update_project_features_by_slug(self.group.uid, slug1, features3)
        project3 = await self.db.get_project_by_slug(self.group.uid, slug1)
        self.assertEqual(features3, project3.features)


if __name__ == "__main__":
    unittest.main()
