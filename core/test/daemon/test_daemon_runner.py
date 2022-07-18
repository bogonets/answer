# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import main

from recc.daemon.daemon_client import create_daemon_client
from recc.daemon.daemon_runner import DaemonRunner, StandardDaemonRunnerCallbacks
from recc.daemon.daemon_servicer import wait_connectable
from recc.packet.daemon import DaemonState
from recc.variables.rpc import DEFAULT_DAEMON_ADDRESS, DEFAULT_DAEMON_PORT
from tester.unittest.plugin_test_case import PluginTestCase


class DaemonRunnerTestCase(PluginTestCase):
    async def _start_server(self):
        self.assertTrue(os.path.isdir(self.working_temp.name))

        module_name = self.recc_daemon_test_router
        self.server_address = DEFAULT_DAEMON_ADDRESS
        self.port = DEFAULT_DAEMON_PORT
        self.client_address = f"localhost:{self.port}"
        self.client = create_daemon_client(self.client_address)
        self.runner = DaemonRunner(
            module_name=module_name,
            working_dir=self.working_temp.name,
            packages_dirs=[self.plugins_dir],
            callbacks=StandardDaemonRunnerCallbacks(),
        )

        self.assertEqual(DaemonState.Down, self.runner.state)
        self.assertFalse(self.runner.running)

        await self.runner.start(self.server_address)
        self.assertTrue(self.runner.running)

        self.assertNotEqual(DaemonState.Down, self.runner.state)
        self.assertTrue(await wait_connectable(self.client_address))

        await self.client.open()
        self.assertTrue(self.client.is_open())
        self.assertEqual(0, await self.client.register())

    async def _stop_server(self):
        if self.client.is_open():
            await self.client.close()
        self.assertFalse(self.client.is_open())
        self.runner.interrupt()
        if self.runner.running:
            await self.runner.join()
        self.assertIsNone(self.runner._task)
        self.assertIsNone(self.runner._process)

        assert self.working_temp
        self.working_temp.cleanup()

    async def asyncSetUp(self):
        self.working_temp = TemporaryDirectory()
        try:
            await self._start_server()
        except:  # noqa
            await self._stop_server()
            raise

    async def asyncTearDown(self):
        await self._stop_server()

    async def test_request(self):
        self.assertTrue(await self.client.heartbeat(0))
        self.assertEqual(0, len(await self.client.get("/test")))


if __name__ == "__main__":
    main()
