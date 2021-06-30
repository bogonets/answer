# -*- coding: utf-8 -*-

import unittest
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.core.context import Context
from tester import AsyncTestCase


class ContextTestCase(AsyncTestCase):
    async def setUp(self):
        config = parse_arguments_to_core_config()
        config.database_name = "recc.test"
        config.teardown = True
        self.context = Context(config, loop=self.loop)
        await self.context.open()
        self.assertTrue(self.context.is_db_open())
        self.assertTrue(self.context.is_cm_open())
        self.assertTrue(self.context.is_cache_open())

    async def tearDown(self):
        await self.context.close()


if __name__ == "__main__":
    unittest.main()
