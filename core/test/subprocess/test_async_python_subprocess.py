# -*- coding: utf-8 -*-

import os
from sys import executable, version_info
from unittest import IsolatedAsyncioTestCase, main
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess


class AsyncPythonSubprocessTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        print("AsyncPythonSubprocessTestCase::setUp cwd: ", os.getcwd())

    def tearDown(self):
        print("AsyncPythonSubprocessTestCase::tearDown cwd: ", os.getcwd())

    async def asyncSetUp(self):
        print("AsyncPythonSubprocessTestCase::asyncSetUp cwd: ", os.getcwd())

    async def asyncTearDown(self):
        print("AsyncPythonSubprocessTestCase::asyncTearDown cwd: ", os.getcwd())

    async def test_version_tuple(self):
        python = AsyncPythonSubprocess(executable)
        version = await python.version_tuple()
        self.assertEqual(version_info[:3], version)

    async def test_list(self):
        print("test_list cwd: ", os.getcwd())
        python = AsyncPythonSubprocess(executable)
        packages = await python.list()
        self.assertLess(0, len(packages))

    async def test_show(self):
        python = AsyncPythonSubprocess(executable)
        show = await python.show("numpy")
        self.assertLess(0, len(show))
        self.assertEqual("numpy", show["Name"])


if __name__ == "__main__":
    main()
