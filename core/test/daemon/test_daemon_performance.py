# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest import main, skipIf

from numpy import ndarray, uint8
from numpy.random import randint

from recc.daemon.daemon_client import create_daemon_client
from recc.daemon.daemon_servicer import create_daemon_server
from tester.unittest.plugin_test_case import PluginTestCase
from tester.variables import (
    DAEMON_ARRAY_PERFORMANCE_ITERATION,
    DAEMON_ARRAY_PERFORMANCE_SKIP_MESSAGE,
    DAEMON_ARRAY_PERFORMANCE_TEST_SKIP,
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


@skipIf(DAEMON_ARRAY_PERFORMANCE_TEST_SKIP, DAEMON_ARRAY_PERFORMANCE_SKIP_MESSAGE)
class DaemonPerformanceTestCase(PluginTestCase):
    async def _start_server(self):
        module_name = "recc_daemon_test_performance"
        self.assertIn(module_name, self.test_daemon_plugin_names)

        accept_info = create_daemon_server("[::]:0", module_name)
        self.servicer = accept_info.servicer
        self.server = accept_info.server
        self.port = accept_info.accepted_port_number
        self.address = f"localhost:{self.port}"
        self.client = create_daemon_client(self.address)

        await self.servicer.open()
        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())
        self.assertEqual(0, await self.client.register())

    async def _stop_server(self):
        await self.servicer.close()
        await self.client.close()
        await self.server.stop(None)
        self.assertFalse(self.client.is_open())

    async def asyncSetUp(self):
        try:
            await self._start_server()
        except:  # noqa
            await self._stop_server()
            raise

    async def asyncTearDown(self):
        await self._stop_server()

    async def _call_split_array(
        self, array: ndarray, body: _Test1, iteration: int
    ) -> float:
        total_seconds = 0.0

        for _ in range(iteration):
            begin = datetime.now()
            result = await self.client.patch("/performance1", array, body)
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
            result = await self.client.patch("/performance2", merged)
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
