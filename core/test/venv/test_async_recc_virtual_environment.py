# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main, skipIf
from recc.venv.async_recc_virtual_environment import AsyncReccVirtualEnvironment
from recc.debugging.trace import is_debugging_mode
from recc.package.requirements_utils import (
    _RECC_PACKAGE_DIR,  # noqa
)
from recc.util.version import version_text

_RECC_DIR = os.path.dirname(_RECC_PACKAGE_DIR)
_CORE_DIR = os.path.dirname(_RECC_DIR)
_PIP_DOWNLOAD_DIR = os.path.join(_CORE_DIR, "storage", "pip.download")
_EXISTS_PIP_DOWNLOAD_DIR = os.path.isdir(_PIP_DOWNLOAD_DIR)
_ENABLE_DEBUGGING_MODE = is_debugging_mode()

if not _EXISTS_PIP_DOWNLOAD_DIR:
    _SKIP_IP = True
    _SKIP_MSG = "If the PIP download directory does not exist, it will not be tested"
elif _ENABLE_DEBUGGING_MODE:
    _SKIP_IP = True
    _SKIP_MSG = "It does not work normally in debugging mode"
else:
    _SKIP_IP = False
    _SKIP_MSG = ""


@skipIf(_SKIP_IP, _SKIP_MSG)
class AsyncReccVirtualEnvironmentTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.venv = AsyncReccVirtualEnvironment(
            self.temp_dir.name,
            pip_download_dir=_PIP_DOWNLOAD_DIR,
        )
        await self.venv.create_if_not_exists()

    async def asyncTearDown(self):
        self.temp_dir.cleanup()

    async def test_recc_module(self):
        python = self.venv.create_python_subprocess()
        version_text_code = "from recc.util.version import version_text;"
        version_text_code += "print(version_text)"
        result = await python.start_python_simply("-c", version_text_code)
        self.assertTrue(version_text, result[0])

        with self.assertRaises(RuntimeError):
            await python.show("recc")

        packages = await python.list()
        package_names = set(map(lambda x: x.name.lower(), packages))
        self.assertIn("aiohttp", package_names)


if __name__ == "__main__":
    main()
