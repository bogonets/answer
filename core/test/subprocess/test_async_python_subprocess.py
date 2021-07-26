# -*- coding: utf-8 -*-

from sys import executable, version_info
from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess


class AsyncPythonSubprocessTestCase(AsyncTestCase):
    async def test_version_tuple(self):
        python = AsyncPythonSubprocess(executable)
        version = await python.version_tuple()
        self.assertEqual(version_info[:3], version)

    async def test_list(self):
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
