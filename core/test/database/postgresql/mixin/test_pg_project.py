# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgProjectTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()
        self.group = await self.db.get_group_by_uid(self.anonymous_group_uid)

    async def test_none_exists_get(self):
        with self.assertRaises(RuntimeError):
            await self.db.get_project_by_uid(999999)

    async def test_create_and_get(self):
        slug1 = "slug1"
        name1 = "name1"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        await self.db.create_project(
            self.group.uid, slug1, name1, created_at=created_at1
        )

        projects1 = await self.db.get_projects()
        self.assertEqual(1, len(projects1))

        project1_uid = await self.db.get_project_uid_by_group_uid_and_slug(
            self.group.uid, slug1
        )
        project1 = await self.db.get_project_by_uid(project1_uid)
        self.assertEqual(self.group.uid, project1.group_uid)
        self.assertEqual(slug1, project1.slug)
        self.assertEqual(name1, project1.name)
        self.assertIsNone(project1.description)
        self.assertIsNone(project1.features)
        self.assertIsNone(project1.extra)
        self.assertEqual(created_at1, project1.created_at)
        self.assertIsNone(project1.updated_at)

        project1_2nd = await self.db.get_project_by_uid(project1.uid)
        self.assertEqual(project1, project1_2nd)

    async def test_update_project(self):
        slug1 = "project1"
        await self.db.create_project(self.group.uid, slug1)
        project1_uid = await self.db.get_project_uid_by_group_uid_and_slug(
            self.group.uid, slug1
        )

        desc1 = "description1"
        extra1 = {"a": 1, "b": 2}
        features1 = ["a", "b"]
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        await self.db.update_project_by_uid(
            uid=project1_uid,
            description=desc1,
            features=features1,
            extra=extra1,
            updated_at=updated_at1,
        )

        project1 = await self.db.get_project_by_uid(project1_uid)
        self.assertEqual(desc1, project1.description)
        self.assertEqual(features1, project1.features)
        self.assertEqual(extra1, project1.extra)
        self.assertEqual(updated_at1, project1.updated_at)

    async def test_delete(self):
        slug1 = "project1"
        await self.db.create_project(self.group.uid, slug1)
        project1_uid = await self.db.get_project_uid_by_group_uid_and_slug(
            self.group.uid, slug1
        )

        projects1 = await self.db.get_project_by_group_uid(self.group.uid)
        self.assertEqual(1, len(projects1))

        await self.db.delete_project_by_uid(project1_uid)

        projects2 = await self.db.get_project_by_group_uid(self.group.uid)
        self.assertEqual(0, len(projects2))


if __name__ == "__main__":
    main()
