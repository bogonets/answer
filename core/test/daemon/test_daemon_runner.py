# -*- coding: utf-8 -*-

import os
from unittest import main, skipIf
from tester.unittest.daemon_server_test_case import DaemonFileTestCase
from recc.daemon.daemon_client import create_daemon_client
from recc.daemon.daemon_runner import DaemonRunner2
from recc.filesystem.permission import is_executable_file
from recc.debugging.trace import is_debugging_mode
from recc.variables.rpc import DEFAULT_DAEMON_PORT, DEFAULT_DAEMON_ADDRESS
from recc.variables.storage import (
    LOCAL_STORAGE_DAEMON_VENV_NAME,
    LOCAL_STORAGE_DAEMON_WORK_NAME,
)


@skipIf(is_debugging_mode(), "It does not work normally in debugging mode.")
class DaemonRunnerTestCase(DaemonFileTestCase):
    def setUp(self):
        super().setUp()

        self.venv_dir = os.path.join(self.temp.name, LOCAL_STORAGE_DAEMON_VENV_NAME)
        self.work_dir = os.path.join(self.temp.name, LOCAL_STORAGE_DAEMON_WORK_NAME)
        os.mkdir(self.venv_dir)
        os.mkdir(self.work_dir)
        self.server_address = DEFAULT_DAEMON_ADDRESS
        self.port = DEFAULT_DAEMON_PORT
        self.client_address = f"localhost:{self.port}"
        self.client = create_daemon_client(self.client_address)
        self.runner = DaemonRunner2(
            self.daemon_dir,
            self.daemon_path,
            self.venv_dir,
            self.work_dir,
        )

    def tearDown(self):
        super().tearDown()

    async def _start_server(self):
        await self.runner.create_venv(16.0)
        await self.runner.join_creator_task()
        self.assertTrue(self.runner.exists)
        self.assertTrue(is_executable_file(self.runner.python_executable))
        self.assertTrue(is_executable_file(self.runner.pip_executable))
        # await self.runner.open(self.server_address)

        # accept_info = create_daemon_server(DEFAULT_DAEMON_ADDRESS, self.daemon_path)
        # self.servicer = accept_info.servicer
        # self.server = accept_info.server
        # self.port = accept_info.accepted_port_number
        # self.address = f"localhost:{self.port}"

        # await self.client.open()
        # self.assertTrue(self.client.is_open())
        # self.assertEqual(0, await self.client.register())

    async def _stop_server(self):
        # if self.client.is_open():
        #     await self.client.close()
        # await self.runner.close()
        # self.assertFalse(self.client.is_open())
        pass

    async def asyncSetUp(self):
        try:
            await self._start_server()
        except:  # noqa
            await self._stop_server()
            raise

    async def asyncTearDown(self):
        await self._stop_server()

    # async def test_heartbeat(self):
    #     self.assertTrue(await self.client.heartbeat(0))
    #
    # async def test_get_test(self):
    #     result = await self.client.get("/test")
    #     self.assertEqual(0, len(result))

    async def test_default(self):
        pass


if __name__ == "__main__":
    main()
