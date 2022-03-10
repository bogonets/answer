# -*- coding: utf-8 -*-

from recc.daemon.daemon_client import create_daemon_client
from recc.daemon.daemon_servicer import create_daemon_server
from recc.variables.rpc import DEFAULT_DAEMON_ADDRESS
from tester.unittest.daemon_file_test_case import DaemonFileTestCase


class DaemonServerTestCase(DaemonFileTestCase):
    async def _start_server(self):
        accept_info = create_daemon_server(DEFAULT_DAEMON_ADDRESS, self.daemon_path)
        self.servicer = accept_info.servicer
        self.server = accept_info.server
        self.port = accept_info.accepted_port_number
        self.address = f"localhost:{self.port}"
        self.client = create_daemon_client(self.address)

        self.assertFalse(self.servicer.plugin.globals["assert_main"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_open"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_close"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_register"])
        await self.servicer.on_open()
        self.assertFalse(self.servicer.plugin.globals["assert_main"])
        self.assertTrue(self.servicer.plugin.globals["assert_on_open"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_close"])
        self.assertFalse(self.servicer.plugin.globals["assert_on_register"])

        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())
        self.assertEqual(0, await self.client.register())
        self.assertTrue(self.servicer.plugin.globals["assert_on_register"])

    async def _stop_server(self):
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

    async def asyncSetUp(self):
        try:
            await self._start_server()
        except:  # noqa
            await self._stop_server()
            raise

    async def asyncTearDown(self):
        await self._stop_server()
