# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, main
from asyncio import get_event_loop
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.core.context import Context


class ContextTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        config = parse_arguments_to_core_config()
        config.database_name = "recc.test"
        config.teardown = True
        self.context = Context(config, loop=get_event_loop())
        await self.context.open()
        self.assertTrue(self.context.is_database_open())
        self.assertTrue(self.context.is_container_open())
        self.assertTrue(self.context.is_cache_open())

    async def asyncTearDown(self):
        await self.context.close()


if __name__ == "__main__":
    main()
