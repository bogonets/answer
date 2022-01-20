# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main
from tester.plugins.copy_plugin import copy_plugin
from recc.plugin.plugin import Plugin
from recc.http.http_client import HttpClient
from recc.variables.http import DEFAULT_HTTP_TEST_PORT


class PluginHttpServerTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.plugin_name = "plugin_http_server"
        self.plugin_filename = self.plugin_name + ".py"
        self.plugin_output = copy_plugin(self.plugin_filename, self.temp_dir.name)
        self.assertTrue(os.path.isfile(self.plugin_output))

    async def asyncTearDown(self):
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
        self.assertEqual(5, len(plugin.routes))

        await plugin.call_open()

        body = "TEST_BODY"
        client = HttpClient(f"{host}:{port}")
        tester_response = await client.get("/tester", text=body)
        self.assertEqual(200, tester_response.status)

        result0 = await plugin.call_route("get", "/")
        self.assertEqual(body, result0)

        data1 = "POST_TEST_BODY"
        result1 = await plugin.call_route("post", "/", data1)
        self.assertEqual(data1, result1)

        result2 = await plugin.call_route("get", "/unknown/a/test")
        self.assertEqual("pattern", result2)

        result3 = await plugin.call_route("get", "/layout/view/aaa")
        self.assertEqual("aaa", result3)

        data4 = "POST_SERVER_DATA"
        result4 = await plugin.call_route("post", "/server/data", data4)
        self.assertEqual(data4, result4)

        await plugin.call_close()
        plugin.call_destroy()


if __name__ == "__main__":
    main()
