# -*- coding: utf-8 -*-

import unittest
import grpc
from recc.argparse.default_namespace import get_default_task_config
from recc.proto import api_pb2 as api
from recc.proto.api_pb2_grpc import ReccApiStub
from recc.rpc.task_server import create_task_server
from tester import AsyncTestCase


class RpcHeartbeatTestCase(AsyncTestCase):
    async def setUp(self):
        self.config = get_default_task_config()
        self.config.task_address = "[::]:0"

        server_info = create_task_server(self.config)
        self.server = server_info.server
        self.port = server_info.accepted_port_number

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
