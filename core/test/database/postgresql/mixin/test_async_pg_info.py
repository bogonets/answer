# -*- coding: utf-8 -*-

import unittest
from tester import AsyncPostgresqlDatabaseTestCase
from recc.util.version import database_version


class AsyncPgInfoTestCase(AsyncPostgresqlDatabaseTestCase):
    async def test_database_version(self):
        self.assertEqual(database_version, await self.db.get_database_version())


if __name__ == "__main__":
    unittest.main()
