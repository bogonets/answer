# -*- coding: utf-8 -*-

import unittest
from tester.unittest.postgresql_test_case import PostgresqlTestCase
from recc.util.version import database_version


class PgInfoTestCase(PostgresqlTestCase):
    async def test_database_version(self):
        self.assertEqual(database_version, await self.db.get_database_version())


if __name__ == "__main__":
    unittest.main()
