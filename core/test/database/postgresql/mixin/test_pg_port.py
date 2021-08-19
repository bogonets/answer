# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgPortTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()

        self.project_slug = "project"
        await self.db.insert_project(self.anonymous_group_uid, self.project_slug)
        self.project_uid = await self.db.get_project_uid_by_group_uid_and_slug(
            self.anonymous_group_uid, self.project_slug
        )
        self.project = await self.db.get_project_by_uid(self.project_uid)

        self.task_slug = "task"
        await self.db.insert_task(self.project.uid, self.task_slug)
        self.task = await self.db.get_task_by_slug(self.project.uid, self.task_slug)

    async def test_create_and_get(self):
        number1 = 100
        number2 = 200
        created_at1 = datetime.utcnow() + timedelta(days=1)
        created_at2 = datetime.utcnow() + timedelta(days=2)
        await self.db.insert_port(number1, created_at=created_at1)
        await self.db.insert_port(
            number2,
            self.anonymous_group_uid,
            self.project.uid,
            self.task.uid,
            created_at=created_at2,
        )
        port1 = await self.db.get_port_by_number(number1)
        self.assertEqual(number1, port1.number)
        self.assertIsNone(port1.group_uid)
        self.assertIsNone(port1.project_uid)
        self.assertIsNone(port1.task_uid)
        self.assertIsNone(port1.description)
        self.assertIsNone(port1.extra)
        self.assertEqual(created_at1, port1.created_at)
        self.assertIsNone(port1.updated_at)

        ports2 = await self.db.get_port_by_group_uid(self.anonymous_group_uid)
        self.assertEqual(1, len(ports2))
        port2 = ports2[0]
        self.assertEqual(number2, port2.number)
        self.assertEqual(self.anonymous_group_uid, port2.group_uid)
        self.assertEqual(self.project.uid, port2.project_uid)
        self.assertEqual(self.task.uid, port2.task_uid)
        self.assertIsNone(port2.description)
        self.assertIsNone(port2.extra)
        self.assertEqual(created_at2, port2.created_at)
        self.assertIsNone(port2.updated_at)

        ports2_2 = await self.db.get_port_by_project_uid(self.project.uid)
        ports2_3 = await self.db.get_port_by_task_uid(self.task.uid)
        self.assertEqual(1, len(ports2_2))
        self.assertEqual(1, len(ports2_3))
        self.assertEqual(port2, ports2_2[0])
        self.assertEqual(port2, ports2_3[0])

    async def test_update_description(self):
        number = 100
        await self.db.insert_port(number)

        desc = "description"
        updated_at = datetime.utcnow()
        await self.db.update_port_description_by_number(number, desc, updated_at)

        port = await self.db.get_port_by_number(number)
        self.assertEqual(desc, port.description)
        self.assertEqual(updated_at, port.updated_at)

    async def test_update_extra(self):
        number = 100
        await self.db.insert_port(number)

        extra = {"a": 1, "b": 2}
        updated_at = datetime.utcnow()
        await self.db.update_port_extra_by_number(number, extra, updated_at)

        port = await self.db.get_port_by_number(number)
        self.assertEqual(extra, port.extra)
        self.assertEqual(updated_at, port.updated_at)

    async def test_update(self):
        number = 100
        created_at = datetime.utcnow()
        await self.db.insert_port(number, created_at=created_at)
        port1 = await self.db.get_port_by_number(number)
        self.assertEqual(number, port1.number)
        self.assertIsNone(port1.group_uid)
        self.assertIsNone(port1.project_uid)
        self.assertIsNone(port1.task_uid)
        self.assertIsNone(port1.description)
        self.assertIsNone(port1.extra)
        self.assertEqual(created_at, port1.created_at)
        self.assertIsNone(port1.updated_at)

        group_uid = self.anonymous_group_uid
        project_uid = self.project.uid
        task_uid = self.task.uid
        extra = {"a": 1, "b": 2}
        updated_at = datetime.utcnow() + timedelta(days=1)
        await self.db.update_port_by_number(
            number,
            group_uid=group_uid,
            project_uid=project_uid,
            task_uid=task_uid,
            extra=extra,
            updated_at=updated_at,
        )

        port2 = await self.db.get_port_by_number(number)
        self.assertEqual(number, port2.number)
        self.assertEqual(group_uid, port2.group_uid)
        self.assertEqual(project_uid, port2.project_uid)
        self.assertEqual(task_uid, port2.task_uid)
        self.assertIsNone(port2.description)
        self.assertEqual(extra, port2.extra)
        self.assertEqual(created_at, port2.created_at)
        self.assertEqual(updated_at, port2.updated_at)

    async def test_delete(self):
        number1 = 100
        number2 = 200
        await self.db.insert_port(number1)
        await self.db.insert_port(number2)
        self.assertEqual(2, len(await self.db.get_ports()))
        await self.db.delete_port_by_number(number1)
        await self.db.delete_port_by_number(number2)
        self.assertEqual(0, len(await self.db.get_ports()))


if __name__ == "__main__":
    unittest.main()
