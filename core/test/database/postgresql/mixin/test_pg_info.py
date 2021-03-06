# -*- coding: utf-8 -*-

from unittest import main
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from recc.util.version import version_text


class PgInfoTestCase(PostgresqlTestCase):
    async def test_database_version(self):
        self.assertEqual(version_text, await self.db.select_database_version())

    async def test_upsert_info(self):
        infos1 = await self.db.select_infos()
        original_count = len(infos1)

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


if __name__ == "__main__":
    main()
