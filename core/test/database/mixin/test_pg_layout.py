# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from unittest import main

from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgLayoutTestCase(PostgresqlTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.group_uid = await self.db.insert_group("group")

        self.project_slug = "project"
        self.project_uid = await self.db.insert_project(
            self.group_uid, self.project_slug
        )
        self.project = await self.db.select_project_by_uid(self.project_uid)

    async def test_create_and_get(self):
        name1 = "layout1"
        name2 = "layout2"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        result1_uid = await self.db.insert_layout(
            self.project.uid, name1, created_at=created_at1
        )
        result2_uid = await self.db.insert_layout(
            self.project.uid, name2, created_at=created_at2
        )
        layout1 = await self.db.select_layout_by_name(self.project.uid, name1)
        layout2 = await self.db.select_layout_by_name(self.project.uid, name2)
        self.assertEqual(result1_uid, layout1.uid)
        self.assertEqual(result2_uid, layout2.uid)

        self.assertEqual(self.project.uid, layout1.project_uid)
        self.assertEqual(self.project.uid, layout2.project_uid)
        self.assertEqual(name1, layout1.name)
        self.assertEqual(name2, layout2.name)
        self.assertIsNone(layout1.description)
        self.assertIsNone(layout2.description)
        self.assertIsNone(layout1.extra)
        self.assertIsNone(layout2.extra)
        self.assertEqual(created_at1, layout1.created_at)
        self.assertEqual(created_at2, layout2.created_at)
        self.assertEqual(created_at1, layout1.updated_at)
        self.assertEqual(created_at2, layout2.updated_at)

        layout1_2nd = await self.db.select_layout_by_uid(layout1.uid)
        layout2_2nd = await self.db.select_layout_by_uid(layout2.uid)
        self.assertEqual(layout1, layout1_2nd)
        self.assertEqual(layout2, layout2_2nd)

    async def test_update_description(self):
        name1 = "layout1"
        name2 = "layout2"
        await self.db.insert_layout(self.project.uid, name1)
        await self.db.insert_layout(self.project.uid, name2)
        layout1_uid = (await self.db.select_layout_by_name(self.project.uid, name1)).uid

        desc1 = "description1"
        desc2 = "description2"
        updated_at1 = datetime.now().astimezone() + timedelta(days=1)
        updated_at2 = datetime.now().astimezone() + timedelta(days=2)
        await self.db.update_layout_description_by_uid(layout1_uid, desc1, updated_at1)
        await self.db.update_layout_description_by_name(
            self.project.uid, name2, desc2, updated_at2
        )

        layout1 = await self.db.select_layout_by_name(self.project.uid, name1)
        layout2 = await self.db.select_layout_by_name(self.project.uid, name2)
        self.assertEqual(desc1, layout1.description)
        self.assertEqual(desc2, layout2.description)
        self.assertEqual(updated_at1, layout1.updated_at)
        self.assertEqual(updated_at2, layout2.updated_at)

    async def test_update_extra(self):
        name1 = "layout1"
        name2 = "layout2"
        await self.db.insert_layout(self.project.uid, name1)
        await self.db.insert_layout(self.project.uid, name2)
        layout1_uid = (await self.db.select_layout_by_name(self.project.uid, name1)).uid

        extra1 = {"a": 1, "b": 2}
        extra2 = {"c": 3, "d": 4}
        updated_at1 = datetime.now().astimezone() + timedelta(days=1)
        updated_at2 = datetime.now().astimezone() + timedelta(days=2)
        await self.db.update_layout_extra_by_uid(layout1_uid, extra1, updated_at1)
        await self.db.update_layout_extra_by_name(
            self.project.uid, name2, extra2, updated_at2
        )

        layout1 = await self.db.select_layout_by_name(self.project.uid, name1)
        layout2 = await self.db.select_layout_by_name(self.project.uid, name2)
        self.assertEqual(extra1, layout1.extra)
        self.assertEqual(extra2, layout2.extra)
        self.assertEqual(updated_at1, layout1.updated_at)
        self.assertEqual(updated_at2, layout2.updated_at)

    async def test_delete(self):
        name1 = "layout1"
        name2 = "layout2"
        await self.db.insert_layout(self.project.uid, name1)
        await self.db.insert_layout(self.project.uid, name2)
        layout1_uid = (await self.db.select_layout_by_name(self.project.uid, name1)).uid

        layouts1 = await self.db.select_layout_by_project_uid(self.project.uid)
        self.assertEqual(2, len(layouts1))

        await self.db.delete_layout_by_uid(layout1_uid)
        await self.db.delete_layout_by_name(self.project.uid, name2)

        layouts2 = await self.db.select_layout_by_project_uid(self.project.uid)
        self.assertEqual(0, len(layouts2))


if __name__ == "__main__":
    main()
