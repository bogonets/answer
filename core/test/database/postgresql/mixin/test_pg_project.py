# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta
from tester import PostgresqlTestCase
from recc.exception.recc_error import ReccNotFoundError


class PgProjectTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()
        self.group = await self.db.get_group_by_uid(self.anonymous_group_uid)

    async def test_none_exists_get(self):
        group_uid = self.group.uid
        group_name = self.group.name
        name = "project"
        unknown = "unknown"
        await self.db.create_project(group_uid, name)

        with self.assertRaises(ReccNotFoundError):
            await self.db.get_project_by_fullpath(unknown, name)
        with self.assertRaises(ReccNotFoundError):
            await self.db.get_project_by_fullpath(group_name, unknown)

        with self.assertRaises(ReccNotFoundError):
            await self.db.get_project_uid_by_fullpath(unknown, name)
        with self.assertRaises(ReccNotFoundError):
            await self.db.get_project_uid_by_fullpath(group_name, unknown)

    async def test_create_and_get(self):
        name1 = "project1"
        name2 = "project2"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        created_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.create_project(self.group.uid, name1, created_at=created_at1)
        await self.db.create_project(self.group.uid, name2, created_at=created_at2)
        project1 = await self.db.get_project_by_name(self.group.uid, name1)
        project2 = await self.db.get_project_by_name(self.group.uid, name2)

        self.assertEqual(self.group.uid, project1.group_uid)
        self.assertEqual(self.group.uid, project2.group_uid)
        self.assertEqual(name1, project1.name)
        self.assertEqual(name2, project2.name)
        self.assertIsNone(project1.description)
        self.assertIsNone(project2.description)
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

        group_name = self.group.name
        project1_3rd = await self.db.get_project_by_fullpath(group_name, name1)
        project2_3rd = await self.db.get_project_by_fullpath(group_name, name2)
        self.assertEqual(project1, project1_3rd)
        self.assertEqual(project2, project2_3rd)

        project1_4th_uid = await self.db.get_project_uid_by_fullpath(group_name, name1)
        project2_4th_uid = await self.db.get_project_uid_by_fullpath(group_name, name2)
        self.assertEqual(project1.uid, project1_4th_uid)
        self.assertEqual(project2.uid, project2_4th_uid)

    async def test_update_description(self):
        name1 = "project1"
        name2 = "project2"
        await self.db.create_project(self.group.uid, name1)
        await self.db.create_project(self.group.uid, name2)
        project1_uid = (await self.db.get_project_by_name(self.group.uid, name1)).uid

        desc1 = "description1"
        desc2 = "description2"
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_project_description_by_uid(
            project1_uid, desc1, updated_at1
        )
        await self.db.update_project_description_by_name(
            self.group.uid, name2, desc2, updated_at2
        )

        project1 = await self.db.get_project_by_name(self.group.uid, name1)
        project2 = await self.db.get_project_by_name(self.group.uid, name2)
        self.assertEqual(desc1, project1.description)
        self.assertEqual(desc2, project2.description)
        self.assertEqual(updated_at1, project1.updated_at)
        self.assertEqual(updated_at2, project2.updated_at)

    async def test_update_extra(self):
        name1 = "project1"
        name2 = "project2"
        await self.db.create_project(self.group.uid, name1)
        await self.db.create_project(self.group.uid, name2)
        project1_uid = (await self.db.get_project_by_name(self.group.uid, name1)).uid

        extra1 = {"a": 1, "b": 2}
        extra2 = {"c": 3, "d": 4}
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_project_extra_by_uid(project1_uid, extra1, updated_at1)
        await self.db.update_project_extra_by_name(
            self.group.uid, name2, extra2, updated_at2
        )

        project1 = await self.db.get_project_by_name(self.group.uid, name1)
        project2 = await self.db.get_project_by_name(self.group.uid, name2)
        self.assertEqual(extra1, project1.extra)
        self.assertEqual(extra2, project2.extra)
        self.assertEqual(updated_at1, project1.updated_at)
        self.assertEqual(updated_at2, project2.updated_at)

    async def test_delete(self):
        name1 = "project1"
        name2 = "project2"
        await self.db.create_project(self.group.uid, name1)
        await self.db.create_project(self.group.uid, name2)
        project1_uid = (await self.db.get_project_by_name(self.group.uid, name1)).uid

        projects1 = await self.db.get_project_by_group_uid(self.group.uid)
        self.assertEqual(2, len(projects1))

        await self.db.delete_project_by_uid(project1_uid)
        await self.db.delete_project_by_name(self.group.uid, name2)

        projects2 = await self.db.get_project_by_group_uid(self.group.uid)
        self.assertEqual(0, len(projects2))


if __name__ == "__main__":
    unittest.main()
