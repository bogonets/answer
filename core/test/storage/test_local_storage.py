# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main

from recc.storage.local_storage import LocalStorage
from tester.lamda.numpy_plugins import copy_builtin_numpy_nodes


class LocalStorageTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.local_storage = LocalStorage(self.temp_dir.name)

        self.assertTrue(os.path.isdir(self.local_storage.root))
        self.assertTrue(os.path.isdir(self.local_storage.get_template_directory()))
        self.assertTrue(os.path.isdir(self.local_storage.workspace))

        template_dir = self.local_storage.get_template_directory()
        self.numpy_json_files = copy_builtin_numpy_nodes(template_dir)
        self.assertLess(0, len(self.numpy_json_files))
        self.local_storage.refresh_templates()

    async def asyncTearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        templates = self.local_storage.get_templates()
        self.assertLess(0, len(templates))

    async def test_tar_bytes(self):
        data = self.local_storage.compress_templates()
        self.assertLess(0, len(data))

        io_bytes = BytesIO(data)
        with tar_open(fileobj=io_bytes, mode="r") as tar:
            tar_names = [f.name for f in tar]
            for json_file in self.numpy_json_files:
                json_name = os.path.basename(json_file)
                expect_name = os.path.join("numpy", json_name)
                self.assertIn(expect_name, tar_names)


if __name__ == "__main__":
    main()
