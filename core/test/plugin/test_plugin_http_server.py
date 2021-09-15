# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.plugins.copy_plugin import copy_plugin
from recc.plugin.plugin import Plugin
from recc.http.http_client import HttpClient
from recc.variables.http import DEFAULT_HTTP_TEST_PORT


class PluginHttpServerTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.plugin_name = "plugin_http_server"
        self.plugin_filename = self.plugin_name + ".py"
        self.plugin_output = copy_plugin(self.plugin_filename, self.temp_dir.name)
        self.assertTrue(os.path.isfile(self.plugin_output))

    async def tearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        host = "0.0.0.0"
        port = DEFAULT_HTTP_TEST_PORT

        plugin = Plugin(self.plugin_output)
        self.assertTrue(plugin.exists_create)
        self.assertTrue(plugin.exists_destroy)
        self.assertTrue(plugin.exists_routes)
        self.assertTrue(plugin.exists_open)
        self.assertTrue(plugin.exists_close)

        plugin.call_create(object(), host=host, port=port)
        self.assertEqual(self.plugin_name, plugin.name)

        plugin.update_routes()
        self.assertEqual(3, len(plugin.routes))

        await plugin.call_open()

        body = "TEST_BODY"
        client = HttpClient(f"{host}:{port}")
        tester_response = await client.get("/tester", text=body)
        self.assertEqual(200, tester_response.status)

        get_result = await plugin.call_route("get", "/")
        self.assertEqual(body, get_result)

        post_data = "POST_TEST_BODY"
        post_result = await plugin.call_route("post", "/", post_data)
        self.assertEqual(post_data, post_result)

        post_result = await plugin.call_route("get", "/unknown/a/test")
        self.assertEqual("pattern", post_result)

        await plugin.call_close()
        plugin.call_destroy()


if __name__ == "__main__":
    main()
