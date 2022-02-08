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
        self.assertIsInstance(result, bytes)
        self.assertEqual(0, len(result))

    async def test_request_test_value_path(self):
        result0 = await self.client.post("/test/sample/path")
        self.assertEqual(result0, "sample")

        result1 = await self.client.get("/test/kkk/path")
        self.assertEqual(result1, "kkk")

    async def test_put_test_body(self):
        body0 = _Test1(0, "aa", {"k": 100}, [1, "Y"], None, [])
        result0 = await self.client.put("/test/body", body0, cls=_Test1)
        self.assertIsInstance(result0, _Test1)
        self.assertEqual(result0, body0)

        result1 = await self.client.put("/test/body", body0)
        self.assertIsInstance(result1, dict)

    async def test_get_test_exception(self):
        with self.assertRaises(AioRpcError):
            await self.client.get("/test/exception")

    async def test_post_test_numpy(self):
        image = randint(0, 255, size=(1270, 1920, 3), dtype=uint8)
        result = await self.client.post("/test/numpy", image, cls=ndarray)
        self.assertIsInstance(result, ndarray)
        self.assertTrue((result == 0).all())


if __name__ == "__main__":
    main()
