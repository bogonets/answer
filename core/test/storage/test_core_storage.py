# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from tempfile import TemporaryDirectory
from shutil import copyfile
from unittest import IsolatedAsyncioTestCase, main
from tester.lamda.numpy_plugins import copy_builtin_numpy_nodes
from tester.plugins import plugin_simple
from recc.package.package_utils import get_module_path
from recc.storage.local_storage import LocalStorage


class CoreStorageTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.sm = LocalStorage(self.temp_dir.name)

        self.assertTrue(os.path.isdir(self.sm.root))
        self.assertTrue(os.path.isdir(self.sm.get_template_directory()))
        self.assertTrue(os.path.isdir(self.sm.get_workspace_directory()))

        template_dir = self.sm.get_template_directory()
        self.numpy_json_files = copy_builtin_numpy_nodes(template_dir)
        self.assertLess(0, len(self.numpy_json_files))
        self.sm.refresh_templates()

        self.assertTrue(self.sm.plugin.is_dir())
        plugin_path = get_module_path(plugin_simple)
        plugin_filename = os.path.split(plugin_path)[1]
        plugin_name = os.path.splitext(plugin_filename)[0]
        plugin_dir = os.path.join(self.sm.plugin, plugin_name)
        plugin_output = os.path.join(plugin_dir, plugin_filename)
        os.mkdir(plugin_dir)
        copyfile(plugin_path, plugin_output)

    async def asyncTearDown(self):
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
        plugins = self.sm.find_plugin_dirs()
        self.assertEqual(1, len(plugins))


if __name__ == "__main__":
    main()
