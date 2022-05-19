# -*- coding: utf-8 -*-

from unittest import main

from recc.http.http_client import HttpClient
from recc.plugin.core_plugin import CorePlugin
from tester.unittest.plugin_test_case import PluginTestCase


class CorePluginHttpServerTestCase(PluginTestCase):
    async def test_default(self):
        module_name = "recc_plugin_test_http_server"
        plugin = CorePlugin(module_name)
        self.assertEqual(module_name, plugin.module_name)

        host = str(plugin.get("TEST_HOST"))
        port = int(plugin.get("TEST_PORT"))

        self.assertTrue(plugin.has_on_create)
        self.assertTrue(plugin.has_on_destroy)
        self.assertTrue(plugin.has_on_open)
        self.assertTrue(plugin.has_on_close)

        self.assertFalse(plugin.has_on_create_group)
        self.assertFalse(plugin.has_on_delete_group)
        self.assertFalse(plugin.has_on_create_project)
        self.assertFalse(plugin.has_on_delete_project)

        self.assertTrue(plugin.has_on_routes)

        plugin.on_create(context=object())
        plugin.update_routes()
        self.assertEqual(5, plugin.count_routes)

        await plugin.on_open()

        body = "TEST_BODY"
        client = HttpClient(f"{host}:{port}")
        tester_response = await client.get("/tester", text=body)
        self.assertEqual(200, tester_response.status)

        result0 = await plugin.route("get", "/")
        self.assertEqual(body, result0)

        data1 = "POST_TEST_BODY"
        result1 = await plugin.route("post", "/", data1)
        self.assertEqual(data1, result1)

        result2 = await plugin.route("get", "/unknown/a/test")
        self.assertEqual("pattern", result2)

        result3 = await plugin.route("get", "/layout/view/aaa")
        self.assertEqual("aaa", result3)

        data4 = "POST_SERVER_DATA"
        result4 = await plugin.route("post", "/server/data", data4)
        self.assertEqual(data4, result4)

        await plugin.on_close()
        plugin.on_destroy()


if __name__ == "__main__":
    main()
