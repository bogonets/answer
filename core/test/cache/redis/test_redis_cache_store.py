# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.cache.redis.redis_cache_store import RedisCacheStore


class RedisCacheStoreTestCase(AsyncTestCase):
    async def setUp(self):
        self.config = parse_arguments_to_core_config()
        self.host = self.config.cache_host
        self.port = self.config.cache_port
        self.pw = self.config.cache_pw

        self.cs = RedisCacheStore(self.host, self.port, self.pw)
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

    async def test_pub_sub(self):
        class _Sub:
            def __init__(self):
                self.data = dict()

            async def reader(self, data):
                self.data = data

        channel = "channel:1"
        value = b"value"

        result = _Sub()
        await self.cs.subscribe(channel, callback=result.reader)
        await self.cs.publish(channel, value)

        self.cs.exit_flag_subscribe(channel)
        await self.cs.wait_subscribe(channel)

        self.assertEqual("message", result.data["type"])
        self.assertIsNone(result.data["pattern"])
        self.assertEqual(channel.encode(), result.data["channel"])
        self.assertEqual(value, result.data["data"])

        task = self.cs.get_subscribe_task(channel)
        self.assertTrue(task.done())


if __name__ == "__main__":
    main()
