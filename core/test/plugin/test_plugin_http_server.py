# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from shutil import copyfile
from unittest import main
from aiohttp.web_response import Response
from tester.unittest.async_test_case import AsyncTestCase
from tester.plugin import plugin_http_server
from recc.package.package_utils import get_module_path
from recc.plugin.plugin import Plugin
from recc.http.http_client import HttpClient
from recc.variables.http import DEFAULT_HTTP_TEST_PORT


class PluginHttpServerTestCase(AsyncTestCase):
    async def setUp(self):
        self.temp_dir = TemporaryDirectory()
        plugin_path = get_module_path(plugin_http_server)
        plugin_name = os.path.split(plugin_path)[1]
        self.plugin_output = os.path.join(self.temp_dir.name, plugin_name)
        copyfile(plugin_path, self.plugin_output)

    async def tearDown(self):
        self.temp_dir.cleanup()

    async def test_default(self):
        host = "0.0.0.0"
        port = DEFAULT_HTTP_TEST_PORT

        plugin = Plugin(self.plugin_output)
        self.assertTrue(plugin.exists_create)
        self.assertTrue(plugin.exists_destroy)
        self.assertTrue(plugin.exists_open)
        self.assertTrue(plugin.exists_close)
        self.assertTrue(plugin.exists_request)

        plugin.call_create(object(), host=host, port=port)
        self.assertEqual("http_server", plugin.name)

        await plugin.call_open()

        body = "TEST_BODY"
        client = HttpClient(f"{host}:{port}")
        tester_response = await client.get("/tester", text=body)
        self.assertEqual(200, tester_response.status)

        response = await plugin.call_request(None)  # noqa
        self.assertIsInstance(response, Response)
        self.assertEqual(body, response.text)

        await plugin.call_close()
        plugin.call_destroy()


if __name__ == "__main__":
    main()
