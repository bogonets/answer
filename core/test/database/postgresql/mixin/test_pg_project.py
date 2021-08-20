# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from recc.variables.database import (
    VISIBILITY_LEVEL_PRIVATE,
    VISIBILITY_LEVEL_INTERNAL,
    VISIBILITY_LEVEL_PUBLIC,
)
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgProjectTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()
        self.group = await self.db.select_group_by_uid(self.anonymous_group_uid)

    async def test_none_exists_get(self):
        with self.assertRaises(RuntimeError):
            await self.db.select_project_by_uid(999999)

    async def test_create_and_get(self):
        slug1 = "slug1"
        name1 = "name1"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        result1_uid = await self.db.insert_project(
            self.group.uid, slug1, name1, created_at=created_at1
        )

        projects1 = await self.db.select_projects()
        self.assertEqual(1, len(projects1))

        project1_uid = await self.db.select_project_uid_by_group_uid_and_slug(
            self.group.uid, slug1
        )
        self.assertEqual(project1_uid, result1_uid)

        project1 = await self.db.select_project_by_uid(project1_uid)
        self.assertEqual(self.group.uid, project1.group_uid)
        self.assertEqual(slug1, project1.slug)
        self.assertEqual(name1, project1.name)
        self.assertIsNone(project1.description)
        self.assertIsNone(project1.features)
        self.assertIsNone(project1.extra)
        self.assertEqual(created_at1, project1.created_at)
        self.assertIsNone(project1.updated_at)

        project1_2nd = await self.db.select_project_by_uid(project1.uid)
        self.assertEqual(project1, project1_2nd)

    async def test_update_project(self):
        slug1 = "project1"
        await self.db.insert_project(self.group.uid, slug1)
        project1_uid = await self.db.select_project_uid_by_group_uid_and_slug(
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

        project1 = await self.db.select_project_by_uid(project1_uid)
        self.assertEqual(desc1, project1.description)
        self.assertEqual(features1, project1.features)
        self.assertEqual(extra1, project1.extra)
        self.assertEqual(updated_at1, project1.updated_at)

    async def test_visibility(self):
        slug1 = "project1"
        slug2 = "project2"
        slug3 = "project3"
        private_uid = await self.db.insert_project(
            self.group.uid, slug1, visibility=VISIBILITY_LEVEL_PRIVATE
        )
        internal_uid = await self.db.insert_project(
            self.group.uid, slug2, visibility=VISIBILITY_LEVEL_INTERNAL
        )
        public_uid = await self.db.insert_project(
            self.group.uid, slug3, visibility=VISIBILITY_LEVEL_PUBLIC
        )

        projects1 = await self.db.select_projects_by_below_visibility(
            VISIBILITY_LEVEL_PRIVATE
        )
        projects2 = await self.db.select_projects_by_below_visibility(
            VISIBILITY_LEVEL_INTERNAL
        )
        projects3 = await self.db.select_projects_by_below_visibility(
            VISIBILITY_LEVEL_PUBLIC
        )

        projects1_uid = list(map(lambda x: x.uid, projects1))
        projects2_uid = list(map(lambda x: x.uid, projects2))
        projects3_uid = list(map(lambda x: x.uid, projects3))

        self.assertEqual(3, len(projects1_uid))
        self.assertIn(private_uid, projects1_uid)
        self.assertIn(internal_uid, projects1_uid)
        self.assertIn(public_uid, projects1_uid)
        self.assertEqual(2, len(projects2_uid))
        self.assertIn(internal_uid, projects2_uid)
        self.assertIn(public_uid, projects2_uid)
        self.assertEqual(1, len(projects3_uid))
        self.assertIn(public_uid, projects3_uid)

    async def test_delete(self):
        slug1 = "project1"
        await self.db.insert_project(self.group.uid, slug1)
        project1_uid = await self.db.select_project_uid_by_group_uid_and_slug(
            self.group.uid, slug1
        )

        projects1 = await self.db.select_projects_by_group_uid(self.group.uid)
        self.assertEqual(1, len(projects1))

        await self.db.delete_project_by_uid(project1_uid)

        projects2 = await self.db.select_projects_by_group_uid(self.group.uid)
        self.assertEqual(0, len(projects2))


if __name__ == "__main__":
    main()
