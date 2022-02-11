# -*- coding: utf-8 -*-

from unittest import main
from numpy.random import randint
from numpy import ndarray, uint8
from typing import Dict, List, Any, Optional
from grpc.aio import AioRpcError
from dataclasses import dataclass
from tester.unittest.daemon_test_case import DaemonTestCase


@dataclass
class _Test1:
    value1: int
    value2: str
    value3: Dict[str, int]
    value4: List[Any]
    value5: Optional[str] = None
    value6: Optional[List[int]] = None


class DaemonCommonTestCase(DaemonTestCase):
    async def test_heartbeat(self):
        self.assertTrue(await self.client.heartbeat(0))

    async def test_get_test(self):
        result = await self.client.get("/test")
        self.assertEqual(0, len(result))

    async def test_request_test_value_path(self):
        result0 = await self.client.post("/test/sample/path")
        self.assertEqual(result0[0], "sample")

        result1 = await self.client.get("/test/kkk/path")
        self.assertEqual(result1[0], "kkk")

    async def test_put_test_body(self):
        body = _Test1(0, "aa", {"k": 100}, [1, "Y"], None, [])
        result = await self.client.put("/test/body", body)
        data = result.cast(0, _Test1)
        self.assertIsInstance(data, _Test1)
        self.assertEqual(data, body)

    async def test_get_test_exception(self):
        with self.assertRaises(AioRpcError):
            await self.client.get("/test/exception")

    async def test_post_test_numpy(self):
        image = randint(0, 255, size=(1270, 1920, 3), dtype=uint8)
        result = await self.client.post("/test/numpy", image)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], ndarray)
        self.assertTrue((result[0] == 0).all())


if __name__ == "__main__":
    main()
