# -*- coding: utf-8 -*-

from recc.database.postgresql.pg_db import PgDb
from recc.argparse.default_parser import parse_arguments_to_core_config
from tester._async.async_test_case import AsyncTestCase  # noqa


class PostgresqlTestCase(AsyncTestCase):
    async def setUp(self):
        self.config = parse_arguments_to_core_config()
        self.host = self.config.database_host
        self.port = self.config.database_port
        self.user = self.config.database_user
        self.pw = self.config.database_pw
        self.name = "recc.test"

        self.db = PgDb(
            db_host=self.host,
            db_port=self.port,
            db_user=self.user,
            db_pw=self.pw,
            db_name=self.name,
        )

        await self.db.open()
        self.assertTrue(self.db.is_open())
        await self.db.drop_tables()
        await self.db.create_tables()
        await self.db.update_cache()

        self.anonymous_group_uid = self.db.get_anonymous_group_uid()
        self.guest_permission_uid = self.db.get_guest_permission_uid()
        self.reporter_permission_uid = self.db.get_reporter_permission_uid()
        self.maintainer_permission_uid = self.db.get_maintainer_permission_uid()
        self.operator_permission_uid = self.db.get_operator_permission_uid()

        self.assertEqual(1, self.anonymous_group_uid)
        self.assertEqual(1, self.guest_permission_uid)
        self.assertEqual(2, self.reporter_permission_uid)
        self.assertEqual(3, self.operator_permission_uid)
        self.assertEqual(4, self.maintainer_permission_uid)

    async def tearDown(self):
        await self.db.close()
        self.assertFalse(self.db.is_open())
