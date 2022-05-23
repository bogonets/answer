# -*- coding: utf-8 -*-

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase

from recc.package.package_utils import all_module_names
from recc.system.path_context import PathContext
from tester.plugins.copy_plugin import copy_plugin


class PluginTestCase(IsolatedAsyncioTestCase):
    def _createPluginPackage(self, plugin_name: str):
        assert self.temp

        package_dir = os.path.join(self.temp.name, plugin_name)
        plugin_init_filepath = os.path.join(package_dir, "__init__.py")

        copy_filepath = copy_plugin(plugin_name, self.temp.name)

        self.assertTrue(os.path.isdir(package_dir))
        self.assertTrue(os.path.isfile(plugin_init_filepath))
        self.assertEqual(Path(copy_filepath), Path(plugin_init_filepath))

    def _setUpPlugins(self):
        assert self.temp
        assert self.path_context

        self.test_core_plugin_names = [
            "recc_plugin_test_http_server",
            "recc_plugin_test_simple",
        ]
        self.test_daemon_plugin_names = [
            "recc_daemon_test_performance",
            "recc_daemon_test_router",
        ]
        self.test_plugin_names = (
            self.test_core_plugin_names + self.test_daemon_plugin_names
        )

        for plugin_name in self.test_plugin_names:
            self._createPluginPackage(plugin_name)
            self.assertIn(plugin_name, all_module_names())

    def _tearDownPlugins(self):
        assert self.temp
        assert self.path_context
        self.path_context.close()
        self.temp.cleanup()

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.path_context = PathContext(self.temp.name, insert_operation=True)
        self.path_context.open()

        try:
            self._setUpPlugins()
        except:  # noqa
            self._tearDownPlugins()
            raise

    def tearDown(self):
        self._tearDownPlugins()
