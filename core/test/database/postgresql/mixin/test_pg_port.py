# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from recc.database.struct.port import SockType
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgPortTestCase(PostgresqlTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.group_uid = await self.db.insert_group("group")
        self.project_uid = await self.db.insert_project(self.group_uid, "project")
        self.task_uid = await self.db.insert_task(self.project_uid, "task")

    async def test_create_and_get(self):
        number1 = 100
        number2 = 200
        sock1 = SockType.Stream
        sock2 = SockType.Dgram
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        await self.db.insert_port(number1, sock1, created_at=created_at1)
        await self.db.insert_port(number2, sock2, created_at=created_at2)
        port1 = await self.db.select_port_by_number_and_sock(number1, sock1)
        port2 = await self.db.select_port_by_number_and_sock(number2, sock2)
        self.assertEqual(number1, port1.number)
        self.assertEqual(number2, port2.number)
        self.assertEqual(sock1, port1.sock)
        self.assertEqual(sock2, port2.sock)
        self.assertIsNone(port1.ref_uid)
        self.assertIsNone(port2.ref_uid)
        self.assertIsNone(port1.ref_category)
        self.assertIsNone(port2.ref_category)
        self.assertEqual(created_at1, port1.created_at)
        self.assertEqual(created_at2, port2.created_at)
        self.assertEqual(created_at1, port1.updated_at)
        self.assertEqual(created_at2, port2.updated_at)

    async def test_delete(self):
        number1 = 100
        number2 = 200
        sock1 = SockType.Stream
        sock2 = SockType.Dgram
        await self.db.insert_port(number1, sock1)
        await self.db.insert_port(number2, sock2)
        self.assertEqual(2, len(await self.db.select_ports()))
        await self.db.delete_port_by_number_and_sock(number1, sock1)
        await self.db.delete_port_by_number_and_sock(number2, sock2)
        self.assertEqual(0, len(await self.db.select_ports()))


if __name__ == "__main__":
    main()
