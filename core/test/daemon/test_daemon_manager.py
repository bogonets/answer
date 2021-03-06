# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.daemon_server_test_case import DaemonFileTestCase

# import os
# from unittest import main, skipIf
# from numpy.random import randint
# from numpy import ndarray, uint8
# from tester.unittest.daemon_server_test_case import DaemonFileTestCase
# from tester.source.storage import get_pip_download_dir
# from tester.pydevd.detect_pydevd import get_isolate_ensure_pip_flag
# from recc.daemon.daemon_client import create_daemon_client
# from recc.daemon.daemon_runner import StandardDaemonRunnerCallbacks, DaemonRunner
# from recc.daemon.daemon_servicer import wait_connectable
# from recc.daemon.daemon_state import DaemonState
# from recc.filesystem.permission import is_executable_file
# from recc.network.access import accessible_network
# from recc.variables.rpc import DEFAULT_DAEMON_PORT, DEFAULT_DAEMON_ADDRESS
# from recc.variables.storage import (
#     LOCAL_STORAGE_DAEMON_VENV_NAME,
#     LOCAL_STORAGE_DAEMON_WORK_NAME,
# )


class DaemonManagerTestCase(DaemonFileTestCase):
    def setUp(self):
        super().setUp()

        # self.venv_dir = os.path.join(self.temp.name, LOCAL_STORAGE_DAEMON_VENV_NAME)
        # self.work_dir = os.path.join(self.temp.name, LOCAL_STORAGE_DAEMON_WORK_NAME)
        # os.mkdir(self.venv_dir)
        # os.mkdir(self.work_dir)
        # self.server_address = DEFAULT_DAEMON_ADDRESS
        # self.port = DEFAULT_DAEMON_PORT
        # self.client_address = f"localhost:{self.port}"
        # self.client = create_daemon_client(self.client_address)
        # self.runner = DaemonRunner(
        #     self.daemon_dir,
        #     self.daemon_path,
        #     self.work_dir,
        #     self.venv_dir,
        #     pip_download_dir=get_pip_download_dir(),
        #     callbacks=StandardDaemonRunnerCallbacks(),
        #     isolate_ensure_pip=get_isolate_ensure_pip_flag(),
        # )

    def tearDown(self):
        super().tearDown()

    async def _start_server(self):
        # self.assertEqual(DaemonState.EnvNotFound, self.runner.state)
        # self.runner.create_venv(32.0)
        # self.assertEqual(DaemonState.EnvCreating, self.runner.state)
        # await self.runner.join_venv_task()
        # self.assertIsNone(self.runner._venv_task)
        # self.assertEqual(DaemonState.Down, self.runner.state)
        # self.assertTrue(self.runner.exists)
        # self.assertTrue(is_executable_file(self.runner.python_executable))
        # self.assertTrue(is_executable_file(self.runner.pip_executable))
        #
        # await self.runner.start_daemon(self.server_address)
        # self.assertNotEqual(DaemonState.Down, self.runner.state)
        # self.assertTrue(await wait_connectable(self.client_address))
        #
        # await self.client.open()
        # self.assertTrue(self.client.is_open())
        # self.assertEqual(0, await self.client.register())
        pass

    async def _stop_server(self):
        # if self.client.is_open():
        #     await self.client.close()
        # self.assertFalse(self.client.is_open())
        # self.runner.kill_daemon()
        # await self.runner.join_daemon_task()
        # self.assertIsNone(self.runner._daemon_task)
        # self.assertIsNone(self.runner._daemon_process)
        pass

    async def asyncSetUp(self):
        try:
            await self._start_server()
        except:  # noqa
            await self._stop_server()
            raise

    async def asyncTearDown(self):
        await self._stop_server()

    # async def test_request(self):
    #     self.assertTrue(await self.client.heartbeat(0))
    #     self.assertEqual(0, len(await self.client.get("/test")))
    #
    # async def test_requirements(self):
    #     files = self.runner.find_requirements()
    #     names = {
    #         os.path.basename(self.requirements1_path),
    #         os.path.basename(self.requirements2_path),
    #     }
    #     self.assertSetEqual(names, set(files))
    #
    # async def test_default_pip(self):
    #     show_package_name = "aiohttp"
    #     packages = await self.runner.list_pip()
    #     package_names = set(map(lambda x: x.name, packages))
    #     self.assertIn(show_package_name, package_names)
    #
    #     pip_info = await self.runner.show_pip(show_package_name)
    #     self.assertEqual(show_package_name, pip_info.name)
    #
    # async def test_post_test_numpy(self):
    #     array = randint(0, 255, size=(1270, 1920, 3), dtype=uint8)
    #     result = await self.client.post("/test/numpy", array)
    #     self.assertEqual(1, len(result))
    #     self.assertIsInstance(result[0], ndarray)
    #     self.assertTrue((result[0] == 0).all())
    #
    # @skipIf(
    #     not accessible_network("https://pypi.org/"),
    #     "You should be able to access the pypi.org site",
    # )
    # async def test_pip_install(self):
    #     install_package_name = "black"
    #     packages = await self.runner.list_pip()
    #     package_names = set(map(lambda x: x.name, packages))
    #     self.assertNotIn(install_package_name, package_names)
    #
    #     self.assertIsNone(self.runner._pip_task)
    #     self.assertIsNone(self.runner._pip_process)
    #     await self.runner.install_pip(install_package_name)
    #     self.assertIsNotNone(self.runner._pip_task)
    #     self.assertIsNotNone(self.runner._pip_process)
    #     await self.runner.join_pip_task()
    #     self.assertIsNone(self.runner._pip_task)
    #     self.assertIsNone(self.runner._pip_process)
    #
    #     packages = await self.runner.list_pip()
    #     package_names = set(map(lambda x: x.name, packages))
    #     self.assertIn(install_package_name, package_names)


if __name__ == "__main__":
    main()
