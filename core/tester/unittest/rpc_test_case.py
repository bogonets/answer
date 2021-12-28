# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase
from recc.argparse.default_namespace import get_default_task_config
from recc.rpc.rpc_client import create_rpc_client
from recc.task.task_server import create_task_server


class RpcTestCase(IsolatedAsyncioTestCase):
    async def _setup(self):
        self.config = get_default_task_config()
        server_info = create_task_server(self.config)
        self.servicer = server_info.servicer
        self.server = server_info.server
        self.port = server_info.accepted_port_number
        self.address = f"localhost:{self.port}"
        self.client = create_rpc_client(self.address)

        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())

    async def asyncSetUp(self):
        try:
            await self._setup()
        except:  # noqa
            await self._teardown()
            raise

    async def _teardown(self):
        await self.client.close()
        await self.server.stop(None)
        self.assertFalse(self.client.is_open())

    async def asyncTearDown(self):
        await self._teardown()
