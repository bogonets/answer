# -*- coding: utf-8 -*-

from unittest import main, skipIf
from datetime import datetime, timedelta
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from tester.variables import UID_PERFORMANCE_TEST_SKIP, UID_PERFORMANCE_ITERATION


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
        created_at = datetime.now().astimezone()

        result_uid = await self.db.insert_user(
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
        user_uid = await self.db.select_user_uid_by_username(username)
        self.assertEqual(result_uid, user_uid)

        user = await self.db.select_user_by_uid(user_uid)
        self.assertEqual(user_uid, user.uid)
        self.assertEqual(username, user.username)
        self.assertEqual(nickname, user.nickname)
        self.assertEqual(email, user.email)
        self.assertEqual(phone1, user.phone1)
        self.assertEqual(phone2, user.phone2)
        self.assertEqual(extra, user.extra)
        self.assertEqual(created_at, user.created_at)
        self.assertIsNone(user.updated_at)
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

    async def test_update_extra(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.insert_user(username, password, salt)

        extra = {"key1": 100, "key2": 200}
        updated_at = datetime.now().astimezone() + timedelta(days=1)

        user_uid = await self.db.select_user_uid_by_username(username)
        await self.db.update_user_extra_by_uid(user_uid, extra, updated_at)
        user_extra = await self.db.select_user_extra_by_uid(user_uid)
        self.assertEqual(extra, user_extra)

        user = await self.db.select_user_by_uid(user_uid)
        self.assertEqual(extra, user.extra)
        self.assertEqual(updated_at, user.updated_at)

    async def test_update_user_info(self):
        username = "admin"
        password = "password"
        salt = "salt"
        await self.db.insert_user(username, password, salt)

        update_phone2 = "010-0000-0001"
        updated_at = datetime.now().astimezone() + timedelta(days=3)
        user_uid = await self.db.select_user_uid_by_username(username)
        await self.db.update_user_by_uid(
            uid=user_uid, phone2=update_phone2, updated_at=updated_at
        )

        users = await self.db.select_users()
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
        await self.db.insert_user(username, "1234", "__unknown_salt__", is_admin=True)
        self.assertTrue(await self.db.select_user_exists_by_username(username))
        self.assertTrue(await self.db.select_exists_admin_user())
        self.assertTrue(await self.db.select_exists_admin_user())


if __name__ == "__main__":
    main()
