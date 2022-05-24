# -*- coding: utf-8 -*-

from asyncio import get_event_loop
from typing import List
from unittest import main

from recc.http import http_urls as u
from recc.http.http_utils import v2_plugins_path, v2_plugins_pplugin_path
from tester.http.http_app_tester import HttpAppTester
from tester.unittest.plugin_test_case import PluginTestCase


class RouterV2PluginsTestCase(PluginTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()
        await self.tester.wait_startup()

        self.username = "user1"
        self.password = "1234"
        try:
            await self.tester.signup_default_admin()
            await self.tester.signup(self.username, self.password)
            await self.tester.signin(self.username, self.password, save_session=True)
        except:  # noqa
            await self.tester.teardown()
            raise

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

    async def test_root(self):
        response = await self.tester.get(v2_plugins_path(u.root), cls=List[str])
        self.assertEqual(200, response.status)
        response_data = response.data
        self.assertIsInstance(response_data, list)
        self.assertListEqual(self.plugin_keys, response_data)

    async def test_plugin_route(self):
        path = v2_plugins_pplugin_path(self.request_plugin_key, "/")
        print("test_plugin_route")
        get_response = await self.tester.get(path)
        self.assertEqual(200, get_response.status)

        test_body = "TEST_BODY"
        post_response = await self.tester.post(path, data=test_body)
        self.assertEqual(200, post_response.status)
        self.assertEqual(test_body, post_response.data)


if __name__ == "__main__":
    main()
