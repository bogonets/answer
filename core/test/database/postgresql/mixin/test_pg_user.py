# -*- coding: utf-8 -*-

import unittest
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from datetime import datetime, timedelta


class PgUserTestCase(PostgresqlTestCase):
    async def test_create_and_get(self):
        username = "admin"
        password = "password"
        salt = "salt"
        nickname = "Unknown"
        email = "admin@localhost"
        phone1 = "010-0000-0000"
        phone2 = "010-0000-0001"
        extra = {"key1": "value1", "key2": "value2"}
        is_admin = False
        created_at = datetime.utcnow()

        await self.db.create_user(
            username,
            password,
            salt,
            nickname=nickname,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
            extra=extra,
            created_at=created_at,
        )

        user = await self.db.get_user_by_username(username)
        self.assertEqual(username, user.username)
        self.assertEqual(nickname, user.nickname)
        self.assertEqual(email, user.email)
        self.assertEqual(phone1, user.phone1)
        self.assertEqual(phone2, user.phone2)
        self.assertEqual(extra, user.extra)
        self.assertEqual(created_at, user.created_at)
        self.assertIsNone(user.updated_at)
        self.assertIsNone(user.last_login)

    async def test_last_login(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.create_user(username, password, salt)

        last_login = datetime.utcnow() + timedelta(days=2)
        await self.db.update_user_last_login_by_username(username, last_login)

        user = await self.db.get_user_by_username(username)
        self.assertEqual(last_login, user.last_login)

    async def test_get_password(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.create_user(username, password, salt)
        pass_info = await self.db.get_user_password_and_salt(username)
        self.assertEqual(password, pass_info.password)
        self.assertEqual(salt, pass_info.salt)

    async def test_update_extra(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.create_user(username, password, salt)

        extra = {"key1": 100, "key2": 200}
        updated_at = datetime.utcnow() + timedelta(days=1)
        await self.db.update_user_extra_by_username(username, extra, updated_at)
        user_extra = await self.db.get_user_extra(username)
        self.assertEqual(extra, user_extra)

        user = await self.db.get_user_by_username(username)
        self.assertEqual(extra, user.extra)
        self.assertEqual(updated_at, user.updated_at)

    async def test_update_user_info(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.create_user(username, password, salt)

        update_phone2 = "010-0000-0001"
        updated_at = datetime.utcnow() + timedelta(days=3)
        await self.db.update_user_by_username(
            username, phone2=update_phone2, updated_at=updated_at
        )

        users = await self.db.get_users()
        self.assertEqual(1, len(users))
        user = users[0]

        self.assertEqual(username, user.username)
        self.assertIsNone(user.email)
        self.assertIsNone(user.phone1)
        self.assertEqual(update_phone2, user.phone2)
        self.assertEqual(updated_at, user.updated_at)

    async def test_delete(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.create_user(username, password, salt)

        self.assertTrue(await self.db.exist_user(username))
        await self.db.delete_user_by_name(username)
        self.assertFalse(await self.db.exist_user(username))

    async def test_exists_admin_user(self):
        self.assertFalse(await self.db.exists_admin_user())

    async def test_signup_admin_user(self):
        username = "admin"
        self.assertFalse(await self.db.exist_user(username))
        self.assertFalse(await self.db.exists_admin_user())
        await self.db.create_user(username, "1234", "__unknown_salt__", is_admin=True)
        self.assertTrue(await self.db.exist_user(username))
        self.assertTrue(await self.db.exists_admin_user())
        self.assertTrue(await self.db.exists_admin_user())


if __name__ == "__main__":
    unittest.main()
