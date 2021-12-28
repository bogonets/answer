# -*- coding: utf-8 -*-

import os
from unittest import IsolatedAsyncioTestCase, main, skipIf
from tempfile import TemporaryDirectory
from recc.argparse.default_namespace import get_default_task_config
from recc.rpc.rpc_client import create_rpc_client
from recc.task.task_server import create_task_server


@skipIf(os.name != "posix", "It only runs on posix")
class RpcPipeClientTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        address = "unix://" + os.path.join(self.temp_dir.name, "sock.pip")

        config = get_default_task_config()
        config.task_address = address
        server_info = create_task_server(config)
        self.server = server_info.server
        self.client = create_rpc_client(address)

        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())

    async def asyncTearDown(self):
        await self.client.close()
        await self.server.stop(None)
        self.temp_dir.cleanup()
        self.assertFalse(self.client.is_open())

    async def test_heartbeat(self):
        self.assertTrue(await self.client.heartbeat(0))


if __name__ == "__main__":
    main()
