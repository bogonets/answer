# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from unittest import main

from tester.unittest.postgresql_test_case import PostgresqlTestCase


class PgUserInfoTestCase(PostgresqlTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        username = "admin"
        password = "password"
        salt = "salt"
        self.user_uid = await self.db.insert_user(username, password, salt)

    async def test_crud_user_info(self):
        user_uid = self.user_uid
        key1 = "key1"
        value1 = "value1"
        created_at = datetime.now().astimezone()

        self.assertEqual(0, len(await self.db.select_user_infos(user_uid)))
        self.assertFalse(await self.db.exists_user_info_by_key(user_uid, key1))

        await self.db.insert_user_info(user_uid, key1, value1, created_at)
        self.assertEqual(1, len(await self.db.select_user_infos(user_uid)))
        self.assertTrue(await self.db.exists_user_info_by_key(user_uid, key1))

        info1 = await self.db.select_user_info_by_key(user_uid, key1)
        self.assertEqual(key1, info1.key)
        self.assertEqual(value1, info1.value)
        self.assertEqual(created_at, info1.created_at)
        self.assertEqual(created_at, info1.updated_at)

        value2 = "value2"
        updated_at = datetime.now().astimezone() + timedelta(days=2)

        await self.db.update_user_info_value_by_key(user_uid, key1, value2, updated_at)
        self.assertEqual(1, len(await self.db.select_user_infos(user_uid)))
        self.assertTrue(await self.db.exists_user_info_by_key(user_uid, key1))

        info1 = await self.db.select_user_info_by_key(user_uid, key1)
        self.assertEqual(key1, info1.key)
        self.assertEqual(value2, info1.value)
        self.assertEqual(created_at, info1.created_at)
        self.assertEqual(updated_at, info1.updated_at)

        await self.db.delete_user_info_by_key(user_uid, key1)
        self.assertEqual(0, len(await self.db.select_user_infos(user_uid)))
        self.assertFalse(await self.db.exists_user_info_by_key(user_uid, key1))

    async def test_upsert_user_info(self):
        user_uid = self.user_uid
        self.assertEqual(0, len(await self.db.select_user_infos(user_uid)))

        key1 = "key1"
        value1 = "value1"
        created_at = datetime.now().astimezone()

        await self.db.upsert_user_info(user_uid, key1, value1, created_at)
        self.assertEqual(1, len(await self.db.select_user_infos(user_uid)))

        info1 = await self.db.select_user_info_by_key(user_uid, key1)
        self.assertEqual(key1, info1.key)
        self.assertEqual(value1, info1.value)
        self.assertEqual(created_at, info1.created_at)
        self.assertEqual(created_at, info1.updated_at)

        value2 = "value2"
        updated_at = datetime.now().astimezone() + timedelta(days=2)

        await self.db.upsert_user_info(user_uid, key1, value2, updated_at)
        self.assertEqual(1, len(await self.db.select_user_infos(user_uid)))

        info1 = await self.db.select_user_info_by_key(user_uid, key1)
        self.assertEqual(key1, info1.key)
        self.assertEqual(value2, info1.value)
        self.assertEqual(created_at, info1.created_at)
        self.assertEqual(updated_at, info1.updated_at)

    async def test_like_user_info(self):
        user_uid = self.user_uid
        self.assertEqual(0, len(await self.db.select_user_infos(user_uid)))

        key_prefix = "test."
        key1 = key_prefix + "key1"
        key2 = key_prefix + "key2"
        value1 = "value1"
        value2 = "value2"

        await self.db.insert_user_info(user_uid, key1, value1)
        await self.db.insert_user_info(user_uid, key2, value2)
        self.assertEqual(2, len(await self.db.select_user_infos(user_uid)))

        infos = await self.db.select_user_infos_like(user_uid, key_prefix + "%")
        self.assertEqual(2, len(infos))

        infos.sort(key=lambda x: x.key)
        self.assertEqual(key1, infos[0].key)
        self.assertEqual(value1, infos[0].value)
        self.assertEqual(key2, infos[1].key)
        self.assertEqual(value2, infos[1].value)


if __name__ == "__main__":
    main()
