# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase
from recc.daemon.daemon_client import create_daemon_client
from recc.daemon.daemon_servicer import create_daemon_server
from recc.variables.rpc import DEFAULT_DAEMON_ADDRESS
from recc.variables.storage import CORE_DAEMON_NAME
from tester.plugins.copy_plugin import copy_plugin


class DaemonTestCase(IsolatedAsyncioTestCase):
    async def _setup(self):
        self.temp = TemporaryDirectory()
        self.daemon_dir = os.path.join(self.temp.name, CORE_DAEMON_NAME)
        os.mkdir(self.daemon_dir)
        self.daemon_filename = "daemon_simple.py"
        self.daemon_path = copy_plugin(self.daemon_filename, self.daemon_dir)
        self.assertTrue(os.path.isfile(self.daemon_path))

        accept_info = create_daemon_server(DEFAULT_DAEMON_ADDRESS, self.daemon_path)
        self.servicer = accept_info.servicer
        self.server = accept_info.server
        self.port = accept_info.accepted_port_number
        self.address = f"localhost:{self.port}"
        self.client = create_daemon_client(self.address)

        self.assertFalse(self.servicer.plugin.globals["assert_main"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_open"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_close"])
        await self.servicer.on_open()
        self.assertFalse(self.servicer.plugin.globals["assert_main"])
        self.assertTrue(self.servicer.plugin.globals["assert_on_open"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_close"])

        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())
        self.assertEqual(0, await self.client.init())

    async def asyncSetUp(self):
        try:
            await self._setup()
        except:  # noqa
            await self._teardown()
            raise

    async def _teardown(self):
        self.assertFalse(self.servicer.plugin.globals["assert_main"])
        self.assertTrue(self.servicer.plugin.globals["assert_on_open"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_close"])
        await self.servicer.on_close()
        self.assertFalse(self.servicer.plugin.globals["assert_main"])
        self.assertTrue(self.servicer.plugin.globals["assert_on_open"])
        self.assertTrue(self.servicer.plugin.globals["assert_on_close"])

        await self.client.close()
        await self.server.stop(None)
        self.assertFalse(self.client.is_open())

    async def asyncTearDown(self):
        await self._teardown()
