# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from recc.variables.database import REFERENCE_CATEGORY_RECC_DAEMON
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgDaemonTestCase(PostgresqlTestCase):
    async def test_create_and_get(self):
        plugin1 = "plugin1"
        plugin2 = "plugin2"
        slug1 = "slug1"
        slug2 = "slug2"
        name1 = "name1"
        name2 = "name2"
        address1 = "localhost1"
        address2 = "localhost2"
        desc1 = "desc1"
        desc2 = "desc2"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        created_at2 = datetime.now().astimezone() + timedelta(days=2)
        uid1 = await self.db.insert_daemon(
            plugin1, slug1, name1, address1, desc1, created_at=created_at1
        )
        uid2 = await self.db.insert_daemon(
            plugin2, slug2, name2, address2, desc2, created_at=created_at2
        )
        self.assertIsNotNone(uid1)
        self.assertIsNotNone(uid2)

        daemon1 = await self.db.select_daemon_by_uid(uid1)
        daemon2 = await self.db.select_daemon_by_slug(slug2)
        self.assertEqual(uid1, daemon1.uid)
        self.assertEqual(uid2, daemon2.uid)
        self.assertEqual(plugin1, daemon1.plugin)
        self.assertEqual(plugin2, daemon2.plugin)
        self.assertEqual(slug1, daemon1.slug)
        self.assertEqual(slug2, daemon2.slug)
        self.assertEqual(name1, daemon1.name)
        self.assertEqual(name2, daemon2.name)
        self.assertEqual(address1, daemon1.address)
        self.assertEqual(address2, daemon2.address)
        self.assertEqual(desc1, daemon1.description)
        self.assertEqual(desc2, daemon2.description)
        self.assertFalse(daemon1.enable)
        self.assertFalse(daemon2.enable)
        self.assertEqual(created_at1, daemon1.created_at)
        self.assertEqual(created_at2, daemon2.created_at)
        self.assertEqual(created_at1, daemon1.updated_at)
        self.assertEqual(created_at2, daemon2.updated_at)

        self.assertEqual(uid1, await self.db.select_daemon_uid_by_slug(slug1))
        self.assertEqual(uid2, await self.db.select_daemon_uid_by_slug(slug2))

    async def test_create_dns_daemon(self):
        self.assertEqual(0, len(await self.db.select_port_all()))

        plugin1 = "plugin1"
        slug1 = "slug1"
        address1 = "localhost:9999"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        uid1 = await self.db.insert_daemon(
            plugin1, slug1, address=address1, created_at=created_at1
        )

        self.assertEqual(1, len(await self.db.select_port_all()))
        ports = await self.db.select_port_by_ref_uid_and_ref_category(
            uid1, REFERENCE_CATEGORY_RECC_DAEMON
        )
        self.assertEqual(1, len(ports))
        self.assertEqual(uid1, ports[0].ref_uid)
        self.assertEqual(REFERENCE_CATEGORY_RECC_DAEMON, ports[0].ref_category)
        self.assertEqual(9999, ports[0].number)
        self.assertEqual(created_at1, ports[0].created_at)
        self.assertEqual(created_at1, ports[0].updated_at)

    async def test_create_ipv6_daemon(self):
        self.assertEqual(0, len(await self.db.select_port_all()))

        plugin1 = "plugin1"
        slug1 = "slug1"
        address1 = "ipv6:[::]:8080,[::1]:8888"
        created_at1 = datetime.now().astimezone() + timedelta(days=1)
        uid1 = await self.db.insert_daemon(
            plugin1, slug1, address=address1, created_at=created_at1
        )

        self.assertEqual(2, len(await self.db.select_port_all()))
        ports = await self.db.select_port_by_ref_uid_and_ref_category(
            uid1, REFERENCE_CATEGORY_RECC_DAEMON
        )
        self.assertEqual(2, len(ports))
        ports.sort(key=lambda x: x.number)

        self.assertEqual(uid1, ports[0].ref_uid)
        self.assertEqual(REFERENCE_CATEGORY_RECC_DAEMON, ports[0].ref_category)
        self.assertEqual(8080, ports[0].number)
        self.assertEqual(created_at1, ports[0].created_at)
        self.assertEqual(created_at1, ports[0].updated_at)

        self.assertEqual(uid1, ports[1].ref_uid)
        self.assertEqual(REFERENCE_CATEGORY_RECC_DAEMON, ports[1].ref_category)
        self.assertEqual(8888, ports[1].number)
        self.assertEqual(created_at1, ports[1].created_at)
        self.assertEqual(created_at1, ports[1].updated_at)

    async def test_update(self):
        plugin = "plugin"
        slug = "slug"
        created_at = datetime.now().astimezone()
        uid = await self.db.insert_daemon(plugin, slug, created_at=created_at)
        daemon1 = await self.db.select_daemon_by_uid(uid)
        self.assertEqual(uid, daemon1.uid)
        self.assertEqual(plugin, daemon1.plugin)
        self.assertEqual(slug, daemon1.slug)
        self.assertEqual("", daemon1.name)
        self.assertEqual("", daemon1.address)
        self.assertEqual("", daemon1.description)
        self.assertFalse(daemon1.enable)
        self.assertEqual(created_at, daemon1.created_at)
        self.assertEqual(created_at, daemon1.updated_at)

        address = "localhost:9999"
        enable = True
        updated_at = datetime.now().astimezone() + timedelta(days=1)
        await self.db.update_daemon_by_uid(
            uid,
            address=address,
            enable=enable,
            updated_at=updated_at,
        )

        daemon2 = await self.db.select_daemon_by_uid(uid)
        self.assertEqual(uid, daemon2.uid)
        self.assertEqual(plugin, daemon2.plugin)
        self.assertEqual(slug, daemon2.slug)
        self.assertEqual("", daemon2.name)
        self.assertEqual(address, daemon2.address)
        self.assertEqual("", daemon2.description)
        self.assertTrue(daemon2.enable)
        self.assertEqual(created_at, daemon2.created_at)
        self.assertEqual(updated_at, daemon2.updated_at)

    async def test_delete(self):
        plugin1 = "plugin1"
        plugin2 = "plugin2"
        slug1 = "slug1"
        slug2 = "slug2"
        uid1 = await self.db.insert_daemon(plugin1, slug1)
        uid2 = await self.db.insert_daemon(plugin2, slug2)
        self.assertIsNotNone(uid1)
        self.assertIsNotNone(uid2)
        self.assertEqual(2, len(await self.db.select_daemons()))
        await self.db.delete_daemon_by_uid(uid1)
        await self.db.delete_daemon_by_slug(slug2)
        self.assertEqual(0, len(await self.db.select_daemons()))


if __name__ == "__main__":
    main()
