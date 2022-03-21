# -*- coding: utf-8 -*-

import sys
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main, skipIf
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc.filesystem.permission import is_executable_file
from recc.debugging.trace import is_debugging_mode


@skipIf(is_debugging_mode(), "It does not work normally in debugging mode")
class AsyncVirtualEnvironmentTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.venv = AsyncVirtualEnvironment(self.temp_dir.name)
        await self.venv.create_if_not_exists()

    async def asyncTearDown(self):
        self.temp_dir.cleanup()

    async def test_print(self):
        print("context", self.venv.context)
        print("bin_name", self.venv.bin_name)
        print("bin_path", self.venv.bin_path)
        print("env_dir", self.venv.env_dir)
        print("env_exe", self.venv.env_exe)
        print("env_name", self.venv.env_name)
        print("executable", self.venv.executable)
        print("inc_path", self.venv.inc_path)
        print("prompt", self.venv.prompt)
        print("python_dir", self.venv.python_dir)
        print("python_exe", self.venv.python_exe)
        print("pip_exe", self.venv.pip_exe)
        print("site_packages_dir", self.venv.site_packages_dir)

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
        self.assertEqual(sys.version_info[:3], version)

    async def test_executables(self):
        self.assertTrue(is_executable_file(self.venv.env_exe))
        self.assertTrue(is_executable_file(self.venv.pip_exe))

    async def test_context_changer(self):
        original_executable = sys.executable

        with self.venv.create_context_changer():
            venv_executable = sys.executable
            try:
                import numpy  # noqa
            except ImportError:
                exists_numpy = False
            else:
                exists_numpy = True

            from dataclasses import dataclass

            # Data class tests where errors are often found.
            @dataclass
            class _TestDataclass:
                data: str

            test_data_class = _TestDataclass("kk")

        self.assertNotEqual(venv_executable, original_executable)
        self.assertEqual(sys.executable, original_executable)
        self.assertFalse(exists_numpy)
        self.assertEqual("kk", test_data_class.data)

    async def test_no_recc_module(self):
        python = self.venv.create_python_subprocess()
        with self.assertRaises(RuntimeError):
            await python.show_as_info("recc")

    async def test_pip_list(self):
        python = self.venv.create_python_subprocess()
        packages = await python.list()
        package_names = set(map(lambda x: x.name, packages))
        self.assertSetEqual({"pip", "setuptools"}, package_names)


if __name__ == "__main__":
    main()
