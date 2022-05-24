# -*- coding: utf-8 -*-

import os
from unittest import IsolatedAsyncioTestCase

from recc.package.package_utils import get_module_directory
from recc.system.path_context import PathContext
from tester import plugins as tester_plugins


class PluginTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self._plugins_dir = get_module_directory(tester_plugins)
        self._path_context = PathContext(self._plugins_dir, insert_operation=True)
        self._path_context.open()

        for plugin in self.test_plugin_names:
            self.assertTrue(os.path.isdir(os.path.join(self._plugins_dir, plugin)))

    def tearDown(self):
        self._path_context.close()

    @property
    def plugins_dir(self) -> str:
        return self._plugins_dir

    def _assert_plugin_name(self, name: str) -> str:
        self.assertTrue(name)
        plugin_dir = os.path.join(self._plugins_dir, name)
        self.assertTrue(os.path.isdir(plugin_dir))
        plugin_init_file = os.path.join(plugin_dir, "__init__.py")
        self.assertTrue(os.path.isfile(plugin_init_file))
        return name

    @property
    def recc_daemon_test_performance(self):
        return self._assert_plugin_name("recc_daemon_test_performance")

    @property
    def recc_daemon_test_router(self):
        return self._assert_plugin_name("recc_daemon_test_router")

    @property
    def recc_plugin_test_http_server(self):
        return self._assert_plugin_name("recc_plugin_test_http_server")

    @property
    def recc_plugin_test_simple(self):
        return self._assert_plugin_name("recc_plugin_test_simple")

    @property
    def test_daemon_plugin_names(self):
        return [
            self.recc_daemon_test_performance,
            self.recc_daemon_test_router,
        ]

    @property
    def test_core_plugin_names(self):
        return [
            self.recc_plugin_test_http_server,
            self.recc_plugin_test_simple,
        ]

    @property
    def test_plugin_names(self):
        return self.test_daemon_plugin_names + self.test_core_plugin_names
