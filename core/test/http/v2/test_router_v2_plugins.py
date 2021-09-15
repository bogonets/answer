# -*- coding: utf-8 -*-

import os
from typing import List
from tempfile import TemporaryDirectory
from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from tester.plugins.copy_plugin import copy_plugin
from recc.http.http_utils import v2_plugins_path, v2_plugins_pplugin_path
from recc.http import http_urls as u
from recc.variables.storage import CORE_PLUGIN_NAME


class RouterV2PluginsTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp = TemporaryDirectory()
        self.plugin_dir = os.path.join(self.temp.name, CORE_PLUGIN_NAME)
        os.mkdir(self.plugin_dir)
        self.plugin_name = "plugin_http_server.py"
        self.plugin_path = copy_plugin("plugin_http_server.py", self.plugin_dir)
        self.assertTrue(os.path.isfile(self.plugin_path))

        self.tester = HttpAppTester(self.loop, self.temp.name)
        await self.tester.setup()
        await self.tester.wait_startup()

        # self.username = "user1"
        # self.password = "1234"
        # await self.tester.signup_default_admin()
        # await self.tester.signup(self.username, self.password)
        # await self.tester.signin(self.username, self.password, save_session=True)

        plugin_keys = list(self.tester.context.plugins.keys())
        self.assertEqual(1, len(plugin_keys))
        self.plugin_name = plugin_keys[0]
        self.assertEqual(self.plugin_name, self.plugin_name)

    async def tearDown(self):
        await self.tester.teardown()
        self.temp.cleanup()

    async def test_root(self):
        response = await self.tester.get(v2_plugins_path(u.root), cls=List[str])
        self.assertEqual(200, response.status)
        response_data = response.data
        self.assertIsInstance(response_data, list)
        self.assertEqual(1, len(response_data))
        self.assertEqual(self.plugin_name, response_data[0])

    async def test_request(self):
        path = v2_plugins_pplugin_path(self.plugin_name, "/tester")
        get_response = await self.tester.get(path)
        self.assertEqual(200, get_response.status)

        post_response = await self.tester.post(path)
        self.assertEqual(200, post_response.status)

        patch_response = await self.tester.patch(path)
        self.assertEqual(200, patch_response.status)

        delete_response = await self.tester.delete(path)
        self.assertEqual(200, delete_response.status)


if __name__ == "__main__":
    main()
