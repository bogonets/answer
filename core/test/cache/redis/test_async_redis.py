# -*- coding: utf-8 -*-

import unittest
from tester.unittest.async_test_case import AsyncTestCase
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.cache.redis.async_redis import AsyncRedisCacheStore


class AsyncRedisCacheStoreTestCase(AsyncTestCase):
    async def setUp(self):
        self.config = parse_arguments_to_core_config()
        self.host = self.config.cache_host
        self.port = self.config.cache_port
        self.pw = self.config.cache_pw

        self.cs = AsyncRedisCacheStore(self.host, self.port, self.pw)
        await self.cs.open()
        self.assertTrue(self.cs.is_open())

    async def tearDown(self):
        await self.cs.close()
        self.assertFalse(self.cs.is_open())

    async def test_set_get(self):
        key = "__test_set_get__key__"
        val = b"__test_set_get__val__"
        try:
            self.assertFalse(await self.cs.exists(key))
            await self.cs.set(key, val)
            self.assertTrue(await self.cs.exists(key))
            self.assertEqual(val, await self.cs.get(key))
            await self.cs.delete(key)
            self.assertFalse(await self.cs.exists(key))
        finally:
            if await self.cs.exists(key):
                await self.cs.delete(key)


if __name__ == "__main__":
    unittest.main()
