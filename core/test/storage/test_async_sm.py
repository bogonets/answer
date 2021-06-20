# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from tempfile import TemporaryDirectory
from unittest import main
from tester import AsyncTestCase
from recc.storage.async_sm import AsyncStorageManager
from tester.node.numpy_plugins import copy_builtin_numpy_nodes


class AsyncStorageManagerTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.sm = AsyncStorageManager(self.temp_dir.name)

        self.assertTrue(os.path.isdir(self.sm.root))
        self.assertTrue(os.path.isdir(self.sm.template_dir))
        self.assertTrue(os.path.isdir(self.sm.workspace_dir))

        self.numpy_json_files = copy_builtin_numpy_nodes(self.sm.template_dir)
        self.assertLess(0, len(self.numpy_json_files))
        self.sm.refresh_templates()

    async def tearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        templates = self.sm.get_templates()
        self.assertLess(0, len(templates))

    async def test_tar_bytes(self):
        data = self.sm.compress_templates()
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
