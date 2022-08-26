# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main
from tester.source.storage import get_pip_download_dir
from tester.pydevd.detect_pydevd import get_isolate_ensure_pip_flag
from recc.venv.async_recc_virtual_environment import AsyncReccVirtualEnvironment
from recc.util.version import version_text
from recc.package.requirements_utils import _RECC_PACKAGE_DIR  # noqa


class AsyncReccVirtualEnvironmentTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.venv = AsyncReccVirtualEnvironment(
            self.temp_dir.name,
            pip_download_dir=get_pip_download_dir(),
            isolate_ensure_pip=get_isolate_ensure_pip_flag(),
        )
        await self.venv.create_if_not_exists()

    async def asyncTearDown(self):
        self.temp_dir.cleanup()

    async def test_recc_module(self):
        python = self.venv.create_python_subprocess()
        result = await python.start_python_simply("-m", "recc", "--version")
        self.assertTrue(version_text, result[0])

    async def test_recc_code(self):
        python = self.venv.create_python_subprocess()
        version_text_code = "from recc.util.version import version_text;"
        version_text_code += "print(version_text)"
        result = await python.start_python_simply("-c", version_text_code)
        self.assertTrue(version_text, result[0])

    async def test_recc_pip(self):
        python = self.venv.create_python_subprocess()
        with self.assertRaises(RuntimeError):
            await python.show("recc")

        packages = await python.list()
        package_names = set(map(lambda x: x.name.lower(), packages))
        self.assertIn("aiohttp", package_names)


if __name__ == "__main__":
    main()
