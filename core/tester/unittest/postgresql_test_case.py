# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase
from recc.database.postgresql.pg_db import PgDb
from recc.argparse.default_parser import parse_arguments_to_core_config


class PostgresqlTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.config = parse_arguments_to_core_config()
        self.host = self.config.database_host
        self.port = self.config.database_port
        self.user = self.config.database_user
        self.pw = self.config.database_pw
        self.name = "recc.test"

        self.db = PgDb(self.host, self.port, self.user, self.pw, self.name)
        await self.db.open()
        self.assertTrue(self.db.is_open())
        await self.db.drop_tables()
        await self.db.create_tables()

    async def asyncTearDown(self):
        await self.db.close()
        self.assertFalse(self.db.is_open())
