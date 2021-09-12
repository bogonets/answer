# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from tempfile import TemporaryDirectory
from shutil import copyfile
from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.lamda.numpy_plugins import copy_builtin_numpy_nodes
from tester.plugin import simple_plugin
from recc.package.package_utils import get_module_path
from recc.storage.core_storage import CoreStorage


class CoreStorageTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.sm = CoreStorage(self.temp_dir.name)

        self.assertTrue(os.path.isdir(self.sm.get_root_directory()))
        self.assertTrue(os.path.isdir(self.sm.get_template_directory()))
        self.assertTrue(os.path.isdir(self.sm.get_workspace_directory()))
        self.assertTrue(os.path.isdir(self.sm.get_workspace_global_directory()))

        template_dir = self.sm.get_template_directory()
        self.numpy_json_files = copy_builtin_numpy_nodes(template_dir)
        self.assertLess(0, len(self.numpy_json_files))
        self.sm.refresh_templates()

        self.assertTrue(self.sm.plugin.is_dir())
        simple_plugin_path = get_module_path(simple_plugin)
        simple_plugin_name = os.path.split(simple_plugin_path)[1]
        simple_plugin_output = os.path.join(self.sm.plugin, simple_plugin_name)
        copyfile(simple_plugin_path, simple_plugin_output)

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

    async def test_plugin(self):
        plugins = self.sm.find_python_plugins()
        self.assertEqual(1, len(plugins))


if __name__ == "__main__":
    main()
