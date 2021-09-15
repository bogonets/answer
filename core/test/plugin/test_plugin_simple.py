# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import main
from aiohttp.web_response import Response
from tester.unittest.async_test_case import AsyncTestCase
from tester.plugins.copy_plugin import copy_plugin
from recc.plugin.plugin import Plugin


class PluginSimpleTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.plugin_name = "plugin_simple.py"
        self.plugin_output = copy_plugin(self.plugin_name, self.temp_dir.name)
        self.assertTrue(os.path.isfile(self.plugin_output))

    async def tearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        plugin = Plugin(self.plugin_output)
        self.assertTrue(plugin.exists_create)
        self.assertTrue(plugin.exists_destroy)
        self.assertTrue(plugin.exists_open)
        self.assertTrue(plugin.exists_close)
        self.assertTrue(plugin.exists_request)

        plugin.call_create(object())
        self.assertEqual(self.plugin_name, plugin.name)

        await plugin.call_open()

        response = await plugin.call_request(None)  # noqa
        self.assertIsInstance(response, Response)
        self.assertEqual("simple", response.text)

        await plugin.call_close()
        plugin.call_destroy()


if __name__ == "__main__":
    main()
