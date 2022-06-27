# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import main

from recc.daemon.daemon_client import create_daemon_client
from recc.daemon.daemon_manager import DaemonManager
from recc.variables.rpc import DEFAULT_DAEMON_PORT
from tester.unittest.plugin_test_case import PluginTestCase


class DaemonManagerTestCase(PluginTestCase):
    async def _start_server(self):
        self.assertTrue(os.path.isdir(self.working_temp.name))

        prefix = "recc_daemon_test_"
        module1 = self.recc_daemon_test_router
        module2 = self.recc_daemon_test_router
        slug1 = "daemon1"
        slug2 = "daemon2"
        port1 = DEFAULT_DAEMON_PORT
        port2 = DEFAULT_DAEMON_PORT + 1
        bind1 = f"[::]:{port1}"
        bind2 = f"[::]:{port2}"
        address1 = f"localhost:{port1}"
        address2 = f"localhost:{port2}"

        self.manager = DaemonManager(
            prefix=prefix,
            working_root_dir=self.working_temp.name,
            packages_dirs=[self.plugins_dir],
        )
        await self.manager.run(slug1, module1, bind1, address1)
        await self.manager.run(slug2, module2, bind2, address2)

        self.client1 = create_daemon_client(address1)
        self.client2 = create_daemon_client(address2)
        await self.client1.open()
        await self.client2.open()

        self.assertTrue(self.client1.is_open())
        self.assertTrue(self.client2.is_open())
        self.assertEqual(0, await self.client1.register())
        self.assertEqual(0, await self.client2.register())

    async def _stop_server(self):
        if self.client1.is_open():
            await self.client1.close()
        if self.client2.is_open():
            await self.client2.close()

        self.assertFalse(self.client1.is_open())
        self.assertFalse(self.client2.is_open())

        await self.manager.close(each_join_timeout=18.0)
        self.assertEqual(0, len(self.manager.zombies))
        self.assertEqual(0, len(self.manager))

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

    async def test_all_request(self):
        self.assertTrue(await self.client1.heartbeat(0))
        self.assertEqual(0, len(await self.client1.get("/test")))

        self.assertTrue(await self.client2.heartbeat(0))
        self.assertEqual(0, len(await self.client2.get("/test")))


if __name__ == "__main__":
    main()
