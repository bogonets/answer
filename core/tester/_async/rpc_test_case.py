# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory
from recc.argparse.default_namespace import get_default_task_config
from recc.rpc.rpc_client import create_rpc_client
from recc.task.task_server import create_task_server
from tester import AsyncTestCase
from tester.node.numpy_plugins import copy_builtin_numpy_nodes


class RpcTestCase(AsyncTestCase):
    async def _setup(self):
        self.temp_dir = TemporaryDirectory()

        self.config = get_default_task_config()
        self.config.task_address = "[::]:0"
        self.config.task_register = "__unknown_key__"
        self.config.task_workspace_dir = self.temp_dir.name

        server_info = create_task_server(self.config)
        self.servicer = server_info.servicer
        self.server = server_info.server
        self.port = server_info.accepted_port_number
        self.address = f"localhost:{self.port}"
        self.client = create_rpc_client(self.address)

        self.template_dir = self.servicer.storage.get_template_directory()
        self.numpy_template_jsons = copy_builtin_numpy_nodes(self.template_dir)
        self.assertLess(0, len(self.numpy_template_jsons))
        self.servicer.storage.refresh_templates()

        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())

    async def setUp(self):
        try:
            await self._setup()
        except:  # noqa
            await self._teardown()
            raise

    async def _teardown(self):
        await self.client.close()
        await self.server.stop(None)
        self.temp_dir.cleanup()
        self.assertFalse(self.client.is_open())

    async def tearDown(self):
        await self._teardown()
