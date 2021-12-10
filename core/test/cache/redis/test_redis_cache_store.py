# -*- coding: utf-8 -*-

from unittest import main
from asyncio import sleep
from tester.unittest.async_test_case import AsyncTestCase
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.cache.redis.redis_cache_store import RedisCacheStore, EXPIRE_ACCURACY_SECONDS


class RedisCacheStoreTestCase(AsyncTestCase):
    async def setUp(self):
        self.config = parse_arguments_to_core_config()
        self.host = self.config.cache_host
        self.port = self.config.cache_port
        self.pw = self.config.cache_pw
        self.prefix = "tester:"

        self.cs = RedisCacheStore(self.host, self.port, self.pw, self.prefix)
        await self.cs.open()
        self.assertTrue(self.cs.is_open())

    async def tearDown(self):
        await self.cs.close()
        self.assertFalse(self.cs.is_open())

    async def test_not_exists_delete(self):
        key1 = "__test_not_exists_delete__key1__"
        key2 = "__test_not_exists_delete__key2__"
        self.assertFalse(await self.cs.exists(key1))
        self.assertFalse(await self.cs.exists(key2))
        await self.cs.delete(key1, key2)
        self.assertFalse(await self.cs.exists(key1))
        self.assertFalse(await self.cs.exists(key2))

    async def test_not_exists_get(self):
        key1 = "__test_not_exists_get__key1__"
        self.assertFalse(await self.cs.exists(key1))
        self.assertIsNone(await self.cs.get(key1))

    async def test_mset_and_exists(self):
        key1 = "__test_mset_and_exists__key1__"
        key2 = "__test_mset_and_exists__key2__"
        val1 = b"val1"
        val2 = b"val2"
        try:
            self.assertFalse(await self.cs.exists(key1))
            self.assertFalse(await self.cs.exists(key2))

            await self.cs.mset({key1: val1, key2: val2})
            self.assertEqual(2, await self.cs.exists(key1, key2))
            self.assertEqual(val1, await self.cs.get(key1))
            self.assertEqual(val2, await self.cs.get(key2))

            await self.cs.delete(key1)
            self.assertEqual(1, await self.cs.exists(key1, key2))
            self.assertFalse(await self.cs.exists(key1))
            self.assertTrue(await self.cs.exists(key2))

            await self.cs.delete(key2)
            self.assertEqual(0, await self.cs.exists(key1, key2))
            self.assertFalse(await self.cs.exists(key1))
            self.assertFalse(await self.cs.exists(key2))
        finally:
            await self.cs.delete(key1, key2)

    async def test_set_get_append(self):
        key = "__test_set_get_append__key__"
        val1 = b"aa"
        val2 = b"bb"
        val_total = val1 + val2
        try:
            self.assertFalse(await self.cs.exists(key))
            await self.cs.set(key, val1)
            self.assertTrue(await self.cs.exists(key))
            self.assertEqual(val1, await self.cs.get(key))

            await self.cs.append(key, val2)
            self.assertTrue(await self.cs.exists(key))
            self.assertEqual(val_total, await self.cs.get(key))

            await self.cs.delete(key)
            self.assertFalse(await self.cs.exists(key))
        finally:
            await self.cs.delete(key)

    async def test_append_get(self):
        key = "__test_append_get__key__"
        val1 = b"cc"
        val2 = b"dd"
        val_total = val1 + val2
        try:
            self.assertFalse(await self.cs.exists(key))
            await self.cs.append(key, val1)
            self.assertTrue(await self.cs.exists(key))
            self.assertEqual(val1, await self.cs.get(key))

            await self.cs.append(key, val2)
            self.assertTrue(await self.cs.exists(key))
            self.assertEqual(val_total, await self.cs.get(key))

            await self.cs.delete(key)
            self.assertFalse(await self.cs.exists(key))
        finally:
            await self.cs.delete(key)

    async def test_massive_set_get(self):
        massive_size = 10 * 1024 * 1024
        key = "__test_massive_set_get__key__"
        val = bytes(massive_size)
        self.assertEqual(massive_size, len(val))
        try:
            self.assertFalse(await self.cs.exists(key))
            await self.cs.set(key, val)  # 10MByte -> 0.02s
            self.assertTrue(await self.cs.exists(key))
            self.assertEqual(val, await self.cs.get(key))  # 10MByte -> 0.04s

            await self.cs.delete(key)
            self.assertFalse(await self.cs.exists(key))
        finally:
            await self.cs.delete(key)

    async def test_expire(self):
        key = "__test_expire__key__"
        val = b"aa"
        expire_seconds = 1
        wait_seconds = expire_seconds + EXPIRE_ACCURACY_SECONDS
        try:
            self.assertFalse(await self.cs.exists(key))
            await self.cs.set(key, val)
            self.assertTrue(await self.cs.exists(key))
            self.assertEqual(val, await self.cs.get(key))

            await self.cs.expire(key, expire_seconds)
            self.assertTrue(await self.cs.exists(key))
            await sleep(wait_seconds)
            self.assertFalse(await self.cs.exists(key))
        finally:
            await self.cs.delete(key)

    async def test_clear(self):
        key1 = "__test_clear__key1__"
        key2 = "__test_clear__key2__"
        val1 = b"val1"
        val2 = b"val2"
        try:
            self.assertFalse(await self.cs.exists(key1))
            self.assertFalse(await self.cs.exists(key2))

            await self.cs.mset({key1: val1, key2: val2})
            self.assertTrue(await self.cs.exists(key1))
            self.assertTrue(await self.cs.exists(key2))

            await self.cs.clear()
            self.assertFalse(await self.cs.exists(key1))
            self.assertFalse(await self.cs.exists(key2))
        finally:
            await self.cs.delete(key1, key2)

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
