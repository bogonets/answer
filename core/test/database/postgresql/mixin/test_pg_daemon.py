# -*- coding: utf-8 -*-

from unittest import main
from hashlib import sha256
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgDaemonTestCase(PostgresqlTestCase):
    async def test_create_and_get(self):
        plugin1 = "plugin1"
        plugin2 = "plugin2"
        name1 = "name1"
        name2 = "name2"
        address1 = "localhost1"
        address2 = "localhost2"
        requirements1 = sha256(b"1").hexdigest()
        requirements2 = sha256(b"2").hexdigest()
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        uid1 = await self.db.insert_daemon(
            plugin1, name1, address1, requirements1, created_at=created_at1
        )
        uid2 = await self.db.insert_daemon(
            plugin2, name2, address2, requirements2, created_at=created_at2
        )
        self.assertIsNotNone(uid1)
        self.assertIsNotNone(uid2)

        daemon1 = await self.db.select_daemon_by_uid(uid1)
        daemon2 = await self.db.select_daemon_by_name(name2)
        self.assertEqual(uid1, daemon1.uid)
        self.assertEqual(uid2, daemon2.uid)
        self.assertEqual(plugin1, daemon1.plugin)
        self.assertEqual(plugin2, daemon2.plugin)
        self.assertEqual(name1, daemon1.name)
        self.assertEqual(name2, daemon2.name)
        self.assertEqual(address1, daemon1.address)
        self.assertEqual(address2, daemon2.address)
        self.assertEqual(requirements1, daemon1.requirements_sha256)
        self.assertEqual(requirements2, daemon2.requirements_sha256)
        self.assertIsNone(daemon1.description)
        self.assertIsNone(daemon2.description)
        self.assertIsNone(daemon1.extra)
        self.assertIsNone(daemon2.extra)
        self.assertFalse(daemon1.enable)
        self.assertFalse(daemon2.enable)
        self.assertEqual(created_at1, daemon1.created_at)
        self.assertEqual(created_at2, daemon2.created_at)
        self.assertIsNone(daemon1.updated_at)
        self.assertIsNone(daemon2.updated_at)

        self.assertEqual(uid1, await self.db.select_daemon_uid_by_name(name1))
        self.assertEqual(uid2, await self.db.select_daemon_uid_by_name(name2))

    async def test_update(self):
        plugin = "plugin"
        name = "name"
        created_at = datetime.now().astimezone()
        uid = await self.db.insert_daemon(plugin, name, created_at=created_at)
        daemon1 = await self.db.select_daemon_by_uid(uid)
        self.assertEqual(uid, daemon1.uid)
        self.assertEqual(plugin, daemon1.plugin)
        self.assertEqual(name, daemon1.name)
        self.assertIsNone(daemon1.address)
        self.assertIsNone(daemon1.requirements_sha256)
        self.assertIsNone(daemon1.description)
        self.assertIsNone(daemon1.extra)
        self.assertFalse(daemon1.enable)
        self.assertEqual(created_at, daemon1.created_at)
        self.assertIsNone(daemon1.updated_at)

        address = "localhost:9999"
        requirements_sha256 = sha256(b"2").hexdigest()
        extra = {"a": 1, "b": 2}
        enable = True
        updated_at = datetime.now().astimezone() + timedelta(days=1)
        await self.db.update_daemon_by_uid(
            uid,
            address=address,
            requirements_sha256=requirements_sha256,
            extra=extra,
            enable=enable,
            updated_at=updated_at,
        )

        daemon2 = await self.db.select_daemon_by_uid(uid)
        self.assertEqual(uid, daemon2.uid)
        self.assertEqual(plugin, daemon2.plugin)
        self.assertEqual(name, daemon2.name)
        self.assertEqual(address, daemon2.address)
        self.assertEqual(requirements_sha256, daemon2.requirements_sha256)
        self.assertIsNone(daemon2.description)
        self.assertEqual(extra, daemon2.extra)
        self.assertTrue(daemon2.enable)
        self.assertEqual(created_at, daemon2.created_at)
        self.assertEqual(updated_at, daemon2.updated_at)

    async def test_delete(self):
        plugin1 = "plugin1"
        plugin2 = "plugin2"
        name1 = "name1"
        name2 = "name2"
        uid1 = await self.db.insert_daemon(plugin1, name1)
        uid2 = await self.db.insert_daemon(plugin2, name2)
        self.assertIsNotNone(uid1)
        self.assertIsNotNone(uid2)
        self.assertEqual(2, len(await self.db.select_daemons()))
        await self.db.delete_daemon_by_uid(uid1)
        await self.db.delete_daemon_by_name(name2)
        self.assertEqual(0, len(await self.db.select_daemons()))


if __name__ == "__main__":
    main()
