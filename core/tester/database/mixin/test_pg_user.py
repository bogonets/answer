# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from unittest import main, skipIf

from tester.unittest.postgresql_test_case import PostgresqlTestCase
from tester.variables import UID_PERFORMANCE_ITERATION, UID_PERFORMANCE_TEST_SKIP


class PgUserTestCase(PostgresqlTestCase):
    async def test_create_and_get(self):
        username = "admin"
        password = "password"
        salt = "salt"
        nickname = "Unknown"
        email = "admin@localhost"
        phone = "010-0000-0000"
        admin = True
        dark = 2
        lang = "ko"
        timezone = "Asia/Seoul"
        created_at = datetime.now().astimezone()

        result_uid = await self.db.insert_user(
            username=username,
            password=password,
            salt=salt,
            nickname=nickname,
            email=email,
            phone=phone,
            admin=admin,
            dark=dark,
            lang=lang,
            timezone=timezone,
            created_at=created_at,
        )
        user_uid = await self.db.select_user_uid_by_username(username)
        self.assertEqual(result_uid, user_uid)

        user = await self.db.select_user_by_uid(user_uid)
        self.assertEqual(user_uid, user.uid)
        self.assertEqual(username, user.username)
        self.assertEqual(nickname, user.nickname)
        self.assertEqual(email, user.email)
        self.assertEqual(phone, user.phone)
        self.assertEqual(admin, user.admin)
        self.assertEqual(dark, user.dark)
        self.assertEqual(lang, user.lang)
        self.assertEqual(timezone, user.timezone)
        self.assertEqual(created_at, user.created_at)
        self.assertEqual(created_at, user.updated_at)
        self.assertIsNone(user.last_login)
        username2 = await self.db.select_user_username_by_uid(user_uid)
        self.assertEqual(username, username2)

    @skipIf(UID_PERFORMANCE_TEST_SKIP, "UID performance testing is off")
    async def test_user_uid_by_username(self):
        user1 = "user1"
        user1_uid1 = await self.db.insert_user(user1, "pw", "salt")
        user1_uid2 = await self.db.select_user_uid_by_username(user1)
        self.assertEqual(user1_uid1, user1_uid2)

        total_count = UID_PERFORMANCE_ITERATION
        total_seconds = 0
        for n in range(total_count):
            begin = datetime.now()
            await self.db.select_user_uid_by_username(user1)
            total_seconds += (datetime.now() - begin).total_seconds()

        avg_duration = total_seconds / total_count
        print(f"PgSQL UID Performance: {avg_duration}s ({total_count}itr)")

    async def test_last_login(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.insert_user(username, password, salt)

        last_login = datetime.now().astimezone() + timedelta(days=2)
        user_uid = await self.db.select_user_uid_by_username(username)
        await self.db.update_user_last_login_by_uid(user_uid, last_login)

        user_uid = await self.db.select_user_uid_by_username(username)
        user = await self.db.select_user_by_uid(user_uid)
        self.assertEqual(last_login, user.last_login)

    async def test_get_password(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.insert_user(username, password, salt)
        user_uid = await self.db.select_user_uid_by_username(username)
        pass_info = await self.db.select_user_password_and_salt_by_uid(user_uid)
        self.assertEqual(password, pass_info.password)
        self.assertEqual(salt, pass_info.salt)

    async def test_delete(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.insert_user(username, password, salt)

        self.assertTrue(await self.db.select_user_exists_by_username(username))
        user_uid = await self.db.select_user_uid_by_username(username)
        await self.db.delete_user_by_uid(user_uid)
        self.assertFalse(await self.db.select_user_exists_by_username(username))

    async def test_exists_admin_user(self):
        self.assertFalse(await self.db.select_exists_admin_user())

    async def test_signup_admin_user(self):
        username = "admin"
        self.assertFalse(await self.db.select_user_exists_by_username(username))
        self.assertFalse(await self.db.select_exists_admin_user())
        await self.db.insert_user(username, "1234", "__unknown_salt__", admin=True)
        self.assertTrue(await self.db.select_user_exists_by_username(username))
        self.assertTrue(await self.db.select_exists_admin_user())
        self.assertTrue(await self.db.select_exists_admin_user())


if __name__ == "__main__":
    main()
