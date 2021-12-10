# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgPortTestCase(PostgresqlTestCase):
    async def setUp(self):
        await super().setUp()
        self.group_uid = await self.db.insert_group("group")
        self.project_uid = await self.db.insert_project(self.group_uid, "project")
        self.task_uid = await self.db.insert_task(self.project_uid, "task")

    async def test_create_and_get(self):
        number1 = 100
        number2 = 200
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        await self.db.insert_port(number1, created_at=created_at1)
        await self.db.insert_port(number2, created_at=created_at2)
        port1 = await self.db.select_port_by_number(number1)
        port2 = await self.db.select_port_by_number(number2)
        self.assertEqual(number1, port1.number)
        self.assertEqual(number2, port2.number)
        self.assertIsNone(port1.description)
        self.assertIsNone(port2.description)
        self.assertIsNone(port1.extra)
        self.assertIsNone(port2.extra)
        self.assertEqual(created_at1, port1.created_at)
        self.assertEqual(created_at2, port2.created_at)
        self.assertIsNone(port1.updated_at)
        self.assertIsNone(port2.updated_at)

    async def test_update_description(self):
        number = 100
        await self.db.insert_port(number)

        desc = "description"
        updated_at = datetime.now().astimezone()
        await self.db.update_port_description_by_number(number, desc, updated_at)

        port = await self.db.select_port_by_number(number)
        self.assertEqual(desc, port.description)
        self.assertEqual(updated_at, port.updated_at)

    async def test_update_extra(self):
        number = 100
        await self.db.insert_port(number)

        extra = {"a": 1, "b": 2}
        updated_at = datetime.now().astimezone()
        await self.db.update_port_extra_by_number(number, extra, updated_at)

        port = await self.db.select_port_by_number(number)
        self.assertEqual(extra, port.extra)
        self.assertEqual(updated_at, port.updated_at)

    async def test_delete(self):
        number1 = 100
        number2 = 200
        await self.db.insert_port(number1)
        await self.db.insert_port(number2)
        self.assertEqual(2, len(await self.db.select_ports()))
        await self.db.delete_port_by_number(number1)
        await self.db.delete_port_by_number(number2)
        self.assertEqual(0, len(await self.db.select_ports()))


if __name__ == "__main__":
    main()
