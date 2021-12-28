# -*- coding: utf-8 -*-

from sys import version_info
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment


class VirtualEnvironmentTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.venv = AsyncVirtualEnvironment(self.temp_dir.name)
        await self.venv.create_if_not_exists()

    async def asyncTearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        self.assertTrue(self.venv.context)
        self.assertTrue(self.venv.bin_name)
        self.assertTrue(self.venv.bin_path)
        self.assertTrue(self.venv.env_dir)
        self.assertTrue(self.venv.env_exe)
        self.assertTrue(self.venv.env_name)
        self.assertTrue(self.venv.executable)
        self.assertTrue(self.venv.inc_path)
        self.assertTrue(self.venv.prompt)
        self.assertTrue(self.venv.python_dir)
        self.assertTrue(self.venv.python_exe)
        self.assertTrue(self.venv.pip_exe)
        self.assertTrue(self.venv.site_packages_dir)

    async def test_version_tuple(self):
        python = self.venv.create_python_subprocess()
        version = await python.version_tuple()
        self.assertEqual(version_info[:3], version)


if __name__ == "__main__":
    main()
