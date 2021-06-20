# -*- coding: utf-8 -*-

import unittest
import grpc
from recc.argparse.config.task_config import TaskConfig
from recc.proto import api_pb2 as api
from recc.proto.api_pb2_grpc import ReccApiStub
from recc.rpc.task_server import create_task_server
from tester import AsyncTestCase


class HeartbeatCheckTestCase(AsyncTestCase):
    async def setUp(self):
        self.config = TaskConfig()
        self.config.task_bind = "[::]"
        self.config.task_port = 0
        self.config.task_register = "__unknown_key__"
        self.config.task_workspace = ""

        server_info = create_task_server(self.config)
        self.server = server_info.server
        self.port = server_info.port

        await self.server.start()
        self.client = grpc.aio.insecure_channel(f"localhost:{self.port}")
        self.assertEqual(grpc.ChannelConnectivity.IDLE, self.client.get_state(True))

    async def tearDown(self):
        await self.client.close()
        await self.server.stop(None)

    async def test_heartbeat(self):
        pat = ReccApiStub(self.client).Heartbeat(api.Pit(delay=0))
        response = await pat
        self.assertTrue(response.ok)

    async def test_heartbeat_timeout(self):
        with self.assertRaises(grpc.aio.AioRpcError):
            pat = ReccApiStub(self.client).Heartbeat(api.Pit(delay=5.0), timeout=1.0)
            await pat


if __name__ == "__main__":
    unittest.main()
