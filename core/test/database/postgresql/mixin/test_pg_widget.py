# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta
from tester import PostgresqlTestCase


class PgWidgetTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()

        self.project_name = "project"
        await self.db.create_project(self.anonymous_group_uid, self.project_name)
        self.project = await self.db.get_project_by_name(
            self.anonymous_group_uid, self.project_name
        )

        self.layout_name = "layout"
        await self.db.create_layout(self.project.uid, self.layout_name)
        self.layout = await self.db.get_layout_by_name(
            self.project.uid, self.layout_name
        )

    async def test_create_and_get(self):
        name1 = "widget1"
        name2 = "widget2"
        created_at1 = datetime.utcnow() + timedelta(days=1)
        created_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.create_widget(self.layout.uid, name1, created_at=created_at1)
        await self.db.create_widget(self.layout.uid, name2, created_at=created_at2)
        widget1 = await self.db.get_widget_by_name(self.layout.uid, name1)
        widget2 = await self.db.get_widget_by_name(self.layout.uid, name2)

        self.assertEqual(self.layout.uid, widget1.layout_uid)
        self.assertEqual(self.layout.uid, widget2.layout_uid)
        self.assertEqual(name1, widget1.name)
        self.assertEqual(name2, widget2.name)
        self.assertIsNone(widget1.description)
        self.assertIsNone(widget2.description)
        self.assertIsNone(widget1.extra)
        self.assertIsNone(widget2.extra)
        self.assertEqual(created_at1, widget1.created_at)
        self.assertEqual(created_at2, widget2.created_at)
        self.assertIsNone(widget1.updated_at)
        self.assertIsNone(widget2.updated_at)

        widget1_2nd = await self.db.get_widget_by_uid(widget1.uid)
        widget2_2nd = await self.db.get_widget_by_uid(widget2.uid)
        self.assertEqual(widget1, widget1_2nd)
        self.assertEqual(widget2, widget2_2nd)

    async def test_update_description(self):
        name1 = "widget1"
        name2 = "widget2"
        await self.db.create_widget(self.layout.uid, name1)
        await self.db.create_widget(self.layout.uid, name2)
        widget1_uid = (await self.db.get_widget_by_name(self.layout.uid, name1)).uid

        desc1 = "description1"
        desc2 = "description2"
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_widget_description_by_uid(widget1_uid, desc1, updated_at1)
        await self.db.update_widget_description_by_name(
            self.layout.uid, name2, desc2, updated_at2
        )

        widget1 = await self.db.get_widget_by_name(self.layout.uid, name1)
        widget2 = await self.db.get_widget_by_name(self.layout.uid, name2)
        self.assertEqual(desc1, widget1.description)
        self.assertEqual(desc2, widget2.description)
        self.assertEqual(updated_at1, widget1.updated_at)
        self.assertEqual(updated_at2, widget2.updated_at)

    async def test_update_extra(self):
        name1 = "widget1"
        name2 = "widget2"
        await self.db.create_widget(self.layout.uid, name1)
        await self.db.create_widget(self.layout.uid, name2)
        widget1_uid = (await self.db.get_widget_by_name(self.layout.uid, name1)).uid

        extra1 = {"a": 1, "b": 2}
        extra2 = {"c": 3, "d": 4}
        updated_at1 = datetime.utcnow() + timedelta(days=1)
        updated_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.update_widget_extra_by_uid(widget1_uid, extra1, updated_at1)
        await self.db.update_widget_extra_by_name(
            self.layout.uid, name2, extra2, updated_at2
        )

        widget1 = await self.db.get_widget_by_name(self.layout.uid, name1)
        widget2 = await self.db.get_widget_by_name(self.layout.uid, name2)
        self.assertEqual(extra1, widget1.extra)
        self.assertEqual(extra2, widget2.extra)
        self.assertEqual(updated_at1, widget1.updated_at)
        self.assertEqual(updated_at2, widget2.updated_at)

    async def test_delete(self):
        name1 = "widget1"
        name2 = "widget2"
        await self.db.create_widget(self.layout.uid, name1)
        await self.db.create_widget(self.layout.uid, name2)
        widget1_uid = (await self.db.get_widget_by_name(self.layout.uid, name1)).uid

        widgets1 = await self.db.get_widget_by_layout_uid(self.layout.uid)
        self.assertEqual(2, len(widgets1))

        await self.db.delete_widget_by_uid(widget1_uid)
        await self.db.delete_widget_by_name(self.layout.uid, name2)

        widgets2 = await self.db.get_widget_by_layout_uid(self.layout.uid)
        self.assertEqual(0, len(widgets2))


if __name__ == "__main__":
    unittest.main()
