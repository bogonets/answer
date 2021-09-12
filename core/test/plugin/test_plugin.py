# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from shutil import copyfile
from unittest import main
from argparse import Namespace
from aiohttp.web_response import Response
from tester.unittest.async_test_case import AsyncTestCase
from tester.plugin import simple_plugin
from recc.package.package_utils import get_module_path
from recc.plugin.plugin import Plugin


class PluginTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp_dir = TemporaryDirectory()
        simple_plugin_path = get_module_path(simple_plugin)
        simple_plugin_name = os.path.split(simple_plugin_path)[1]
        self.simple_plugin_output = os.path.join(self.temp_dir.name, simple_plugin_name)
        copyfile(simple_plugin_path, self.simple_plugin_output)

    async def tearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        plugin = Plugin(self.simple_plugin_output)
        self.assertTrue(plugin.exists_setup)
        self.assertTrue(plugin.exists_teardown)
        self.assertTrue(plugin.exists_request)

        config = Namespace()
        context = dict()
        await plugin.call_setup(config, context)

        response = await plugin.call_request()
        self.assertIsInstance(response, Response)

        await plugin.call_teardown()


if __name__ == "__main__":
    main()
