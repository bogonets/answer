# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, main

import grpc

from recc.proto.rpc import rpc_api_pb2 as api
from recc.proto.rpc.rpc_api_pb2_grpc import RpcApiStub


class RpcNoServerTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.host = "localhost"
        self.port = 19999
        self.client = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        self.assertEqual(grpc.ChannelConnectivity.IDLE, self.client.get_state(True))

    async def asyncTearDown(self):
        await self.client.close()

    async def test_healthcheck(self):
        with self.assertRaises(grpc.aio.AioRpcError):
            pat = RpcApiStub(self.client).Heartbeat(api.Pit(delay=0), timeout=1.0)
            await pat


if __name__ == "__main__":
    main()
