# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from unittest import main

from grpc.aio import AioRpcError
from numpy import ndarray, uint8
from numpy.random import randint

from recc.daemon.daemon_client import create_daemon_client
from recc.daemon.daemon_servicer import create_daemon_server
from tester.unittest.plugin_test_case import PluginTestCase


@dataclass
class _Test1:
    value1: int
    value2: str
    value3: Dict[str, int]
    value4: List[Any]
    value5: Optional[str] = None
    value6: Optional[List[int]] = None


@dataclass
class _Result1:
    value1: int
    value2: str


class DaemonRouterTestCase(PluginTestCase):
    async def _start_server(self):
        module_name = "recc_daemon_test_router"
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


if __name__ == "__main__":
    main()
