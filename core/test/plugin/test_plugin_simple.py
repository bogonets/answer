# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from shutil import copyfile
from unittest import main
from aiohttp.web_response import Response
from tester.unittest.async_test_case import AsyncTestCase
from tester.plugin import plugin_simple
from recc.package.package_utils import get_module_path
from recc.plugin.plugin import Plugin


class PluginSimpleTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp_dir = TemporaryDirectory()
        plugin_path = get_module_path(plugin_simple)
        plugin_name = os.path.split(plugin_path)[1]
        self.plugin_output = os.path.join(self.temp_dir.name, plugin_name)
        copyfile(plugin_path, self.plugin_output)

    async def tearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        plugin = Plugin(self.plugin_output)
        self.assertTrue(plugin.exists_setup)
        self.assertTrue(plugin.exists_teardown)
        self.assertTrue(plugin.exists_request)

        context = dict()
        await plugin.call_setup(context)
        self.assertEqual("simple", plugin.name)

        response = await plugin.call_request(None)  # noqa
        self.assertIsInstance(response, Response)
        self.assertEqual("simple", response.text)

        await plugin.call_teardown()


if __name__ == "__main__":
    main()
