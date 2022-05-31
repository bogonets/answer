# -*- coding: utf-8 -*-

from asyncio import get_event_loop
from unittest import main

from recc.http import http_urls as u
from tester.http.http_app_tester import HttpAppTester
from tester.unittest.plugin_test_case import PluginTestCase


class HttpPluginsWwwTestCase(PluginTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()
        await self.tester.wait_startup()

        self.plugin_keys = list(self.tester.context._plugins.keys())
        self.assertEqual(len(self.test_core_plugin_names), len(self.plugin_keys))

        prefix = self.tester.context.config.core_plugin_prefix
        prefix_length = len(prefix)

        for test_plugin_name in self.test_core_plugin_names:
            test_plugin_key = test_plugin_name[prefix_length:]
            self.assertIn(test_plugin_key, self.plugin_keys)

        self.request_plugin_name = self.recc_plugin_test_http_server
        self.request_plugin_key = self.request_plugin_name[prefix_length:]
        self.assertIn(self.request_plugin_name, self.test_core_plugin_names)
        self.assertIn(self.request_plugin_key, self.plugin_keys)

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_plugin_spec_www(self):
        path_prefix = u.plugins + u.pplugin.format(plugin=self.request_plugin_key)

        index_html_content = "INDEX"
        default_js_content = "'use strict';"

        path1 = path_prefix + "/any_suffix_paths_to_index.html"
        get_response = await self.tester.get(path1)
        self.assertEqual(200, get_response.status)
        self.assertIsInstance(get_response.data, str)
        self.assertEqual(index_html_content, get_response.data.strip())

        path2 = path_prefix + "/default.js"
        get_response = await self.tester.get(path2)
        self.assertEqual(200, get_response.status)
        self.assertIsInstance(get_response.data, str)
        self.assertEqual(default_js_content, get_response.data.strip())

        path3 = path_prefix + "/index.html"
        get_response = await self.tester.get(path3)
        self.assertEqual(200, get_response.status)
        self.assertIsInstance(get_response.data, str)
        self.assertEqual(index_html_content, get_response.data.strip())


if __name__ == "__main__":
    main()
