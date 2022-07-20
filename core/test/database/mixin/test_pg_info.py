# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from unittest import main

from recc.util.version import version_text
from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgInfoTestCase(PostgresqlTestCase):
    async def test_crud_info(self):
        original_count = len(await self.db.select_infos())

        key1 = "key1"
        value1 = "value1"
        created_at = datetime.now().astimezone()

        self.assertFalse(await self.db.exists_info_by_key(key1))

        await self.db.insert_info(key1, value1, created_at)
        self.assertEqual(original_count + 1, len(await self.db.select_infos()))
        self.assertTrue(await self.db.exists_info_by_key(key1))

        info1 = await self.db.select_info_by_key(key1)
        self.assertEqual(key1, info1.key)
        self.assertEqual(value1, info1.value)
        self.assertEqual(created_at, info1.created_at)
        self.assertEqual(created_at, info1.updated_at)

        value2 = "value2"
        updated_at = datetime.now().astimezone() + timedelta(days=2)

        await self.db.update_info_value_by_key(key1, value2, updated_at)
        self.assertEqual(original_count + 1, len(await self.db.select_infos()))
        self.assertTrue(await self.db.exists_info_by_key(key1))

        info1 = await self.db.select_info_by_key(key1)
        self.assertEqual(key1, info1.key)
        self.assertEqual(value2, info1.value)
        self.assertEqual(created_at, info1.created_at)
        self.assertEqual(updated_at, info1.updated_at)

        await self.db.delete_info_by_key(key1)
        self.assertEqual(original_count, len(await self.db.select_infos()))
        self.assertFalse(await self.db.exists_info_by_key(key1))

    async def test_upsert_info(self):
        original_count = len(await self.db.select_infos())

        key = "aaa"
        val1 = "bbb"
        val2 = "ccc"
        created_at = datetime.now().astimezone() + timedelta(days=1)
        updated_at = datetime.now().astimezone() + timedelta(days=2)

        await self.db.upsert_info(key, val1, created_at)
        self.assertEqual(original_count + 1, len(await self.db.select_infos()))
        info1 = await self.db.select_info_by_key(key)
        self.assertEqual(key, info1.key)
        self.assertEqual(val1, info1.value)
        self.assertEqual(created_at, info1.created_at)
        self.assertEqual(created_at, info1.updated_at)

        await self.db.upsert_info(key, val2, updated_at)
        self.assertEqual(original_count + 1, len(await self.db.select_infos()))
        info2 = await self.db.select_info_by_key(key)
        self.assertEqual(key, info2.key)
        self.assertEqual(val2, info2.value)
        self.assertEqual(created_at, info2.created_at)
        self.assertEqual(updated_at, info2.updated_at)

    async def test_like_info(self):
        original_count = len(await self.db.select_infos())

        key_prefix = "test."
        key1 = key_prefix + "key1"
        key2 = key_prefix + "key2"
        value1 = "value1"
        value2 = "value2"

        await self.db.insert_info(key1, value1)
        await self.db.insert_info(key2, value2)
        self.assertEqual(original_count + 2, len(await self.db.select_infos()))

        infos = await self.db.select_infos_like(key_prefix + "%")
        self.assertEqual(2, len(infos))

        infos.sort(key=lambda x: x.key)
        self.assertEqual(key1, infos[0].key)
        self.assertEqual(value1, infos[0].value)
        self.assertEqual(key2, infos[1].key)
        self.assertEqual(value2, infos[1].value)

    async def test_database_version(self):
        self.assertEqual(version_text, await self.db.select_database_version())


if __name__ == "__main__":
    main()
