# -*- coding: utf-8 -*-

from unittest import main, skipIf
from numpy.random import randint
from numpy import ndarray, uint8
from datetime import datetime
from typing import Dict, List, Any, Optional
from grpc.aio import AioRpcError
from dataclasses import dataclass
from tester.unittest.daemon_server_test_case import DaemonServerTestCase
from tester.variables import (
    DAEMON_ARRAY_PERFORMANCE_TEST_SKIP,
    DAEMON_ARRAY_PERFORMANCE_ITERATION,
    DAEMON_ARRAY_PERFORMANCE_SKIP_MESSAGE,
)


@dataclass
class _Test1:
    value1: int
    value2: str
    value3: Dict[str, int]
    value4: List[Any]
    value5: Optional[str] = None
    value6: Optional[List[int]] = None


@dataclass
class _Test2:
    array: ndarray
    body: _Test1


@dataclass
class _Result1:
    value1: int
    value2: str


PERFORMANCE_TEST_ARRAY = randint(0, 255, size=(1270, 1920, 3), dtype=uint8)
PERFORMANCE_TEST_BODY = _Test1(0, "aa", {"k": 100}, [1, "Y"], None, [])


class DaemonCommonTestCase(DaemonServerTestCase):
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
        array = randint(0, 255, size=(1270, 1920, 3), dtype=uint8)
        result = await self.client.post("/test/numpy", array)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], ndarray)
        self.assertTrue((result[0] == 0).all())

    async def test_post_test_numpy_body(self):
        array = randint(0, 255, size=(1270, 1920, 3), dtype=uint8)
        body = _Test1(0, "aa", {"k": 100}, [1, "Y"], None, [])

        result = await self.client.patch("/test/numpy/body", array, body)
        self.assertEqual(2, len(result))

        self.assertIsInstance(result[0], ndarray)
        self.assertTrue((result[0] == 0).all())

        self.assertIsInstance(result[1], dict)
        self.assertEqual(body.value1, result[1]["value1"])
        self.assertEqual(body.value2, result[1]["value2"])

        data = result.cast(1, _Result1)
        self.assertIsInstance(data, _Result1)
        self.assertEqual(body.value1, data.value1)
        self.assertEqual(body.value2, data.value2)

    async def _call_split_array(
        self, array: ndarray, body: _Test1, iteration: int
    ) -> float:
        total_seconds = 0.0

        for _ in range(iteration):
            begin = datetime.now()
            result = await self.client.patch("/test/numpy/body", array, body)
            total_seconds += (datetime.now() - begin).total_seconds()

            self.assertEqual(2, len(result))
            self.assertIsInstance(result[0], ndarray)
            self.assertTrue((result[0] == 0).all())

            data = result.cast(1, _Result1)
            self.assertIsInstance(data, _Result1)
            self.assertEqual(body.value1, data.value1)
            self.assertEqual(body.value2, data.value2)

        return total_seconds

    async def _call_merged_array(
        self, array: ndarray, body: _Test1, iteration: int
    ) -> float:
        total_seconds = 0.0
        merged = _Test2(array, body)

        for _ in range(iteration):
            begin = datetime.now()
            result = await self.client.patch("/test/numpy/body2", merged)
            total_seconds += (datetime.now() - begin).total_seconds()

            self.assertEqual(2, len(result))
            self.assertIsInstance(result[0], ndarray)
            self.assertTrue((result[0] == 0).all())

            data = result.cast(1, _Result1)
            self.assertIsInstance(data, _Result1)
            self.assertEqual(body.value1, data.value1)
            self.assertEqual(body.value2, data.value2)

        return total_seconds

    @skipIf(DAEMON_ARRAY_PERFORMANCE_TEST_SKIP, DAEMON_ARRAY_PERFORMANCE_SKIP_MESSAGE)
    async def test_shared_memory_split_packet(self):
        self.assertTrue(self.client.possible_shared_memory)
        self.assertFalse(self.client.disable_shared_memory)
        array = PERFORMANCE_TEST_ARRAY
        body = PERFORMANCE_TEST_BODY
        iteration = DAEMON_ARRAY_PERFORMANCE_ITERATION
        total_seconds = await self._call_split_array(array, body, iteration)
        avg_seconds = round(total_seconds / DAEMON_ARRAY_PERFORMANCE_ITERATION, 4)
        print(f"Split packet - Average seconds: {avg_seconds}s (Enable shared-memory)")

    @skipIf(DAEMON_ARRAY_PERFORMANCE_TEST_SKIP, DAEMON_ARRAY_PERFORMANCE_SKIP_MESSAGE)
    async def test_shared_memory_merged_packet(self):
        self.assertTrue(self.client.possible_shared_memory)
        self.assertFalse(self.client.disable_shared_memory)
        array = PERFORMANCE_TEST_ARRAY
        body = PERFORMANCE_TEST_BODY
        iteration = DAEMON_ARRAY_PERFORMANCE_ITERATION
        total_seconds = await self._call_merged_array(array, body, iteration)
        avg_seconds = round(total_seconds / DAEMON_ARRAY_PERFORMANCE_ITERATION, 4)
        print(f"Merge packet - Average seconds: {avg_seconds}s (Enable shared-memory)")

    @skipIf(DAEMON_ARRAY_PERFORMANCE_TEST_SKIP, DAEMON_ARRAY_PERFORMANCE_SKIP_MESSAGE)
    async def test_split_packet(self):
        self.assertTrue(self.client.possible_shared_memory)
        self.client.disable_shared_memory = True
        array = PERFORMANCE_TEST_ARRAY
        body = PERFORMANCE_TEST_BODY
        iteration = DAEMON_ARRAY_PERFORMANCE_ITERATION
        total_seconds = await self._call_split_array(array, body, iteration)
        avg_seconds = round(total_seconds / DAEMON_ARRAY_PERFORMANCE_ITERATION, 4)
        print(f"Split packet - Average seconds: {avg_seconds}s (Disable shared-memory)")

    @skipIf(DAEMON_ARRAY_PERFORMANCE_TEST_SKIP, DAEMON_ARRAY_PERFORMANCE_SKIP_MESSAGE)
    async def test_merged_packet(self):
        self.assertTrue(self.client.possible_shared_memory)
        self.client.disable_shared_memory = True
        array = PERFORMANCE_TEST_ARRAY
        body = PERFORMANCE_TEST_BODY
        iteration = DAEMON_ARRAY_PERFORMANCE_ITERATION
        total_seconds = await self._call_merged_array(array, body, iteration)
        avg_seconds = round(total_seconds / DAEMON_ARRAY_PERFORMANCE_ITERATION, 4)
        print(f"Merge packet - Average seconds: {avg_seconds}s (Disable shared-memory)")


if __name__ == "__main__":
    main()
