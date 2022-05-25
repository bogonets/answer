# -*- coding: utf-8 -*-

from unittest import main

from recc.http.http_client import HttpClient
from recc.plugin.core_plugin import CorePlugin
from tester.unittest.plugin_test_case import PluginTestCase


class CorePluginHttpServerTestCase(PluginTestCase):
    def setUp(self):
        super().setUp()

        self.module_name = self.recc_plugin_test_http_server
        self.plugin = CorePlugin(self.module_name)
        self.assertEqual(self.module_name, self.plugin.module_name)

        self.assertTrue(self.plugin.has_on_create)
        self.assertTrue(self.plugin.has_on_destroy)
        self.assertTrue(self.plugin.has_on_open)
        self.assertTrue(self.plugin.has_on_close)

        self.assertFalse(self.plugin.has_on_create_group)
        self.assertFalse(self.plugin.has_on_delete_group)
        self.assertFalse(self.plugin.has_on_create_project)
        self.assertFalse(self.plugin.has_on_delete_project)

        self.assertTrue(self.plugin.has_on_routes)

        self.host = str(self.plugin.get("TEST_HOST"))
        self.port = int(self.plugin.get("TEST_PORT"))
        self.address = f"{self.host}:{self.port}"

        self.plugin.on_create(context=object())
        self.plugin.update_routes()
        self.assertEqual(5, self.plugin.count_routes)

    def tearDown(self):
        self.plugin.on_destroy()
        super().tearDown()

    async def asyncSetUp(self):
        await self.plugin.on_open()

    async def asyncTearDown(self):
        await self.plugin.on_close()

    async def test_request(self):
        body = "TEST_BODY"
        client = HttpClient(self.address)
        tester_response = await client.get("/tester", text=body)
        self.assertEqual(200, tester_response.status)

        result0 = await self.plugin.route("get", "/")
        self.assertEqual(body, result0)

    async def test_route(self):
        data1 = "POST_TEST_BODY"
        result1 = await self.plugin.route("post", "/", data1)
        self.assertEqual(data1, result1)

        result2 = await self.plugin.route("get", "/unknown/a/test")
        self.assertEqual("pattern", result2)

        result3 = await self.plugin.route("get", "/layout/view/aaa")
        self.assertEqual("aaa", result3)

        data4 = "POST_SERVER_DATA"
        result4 = await self.plugin.route("post", "/server/data", data4)
        self.assertEqual(data4, result4)

    def test_spec_www(self):
        self.assertEqual(2, len(self.plugin.spec.www))

        self.assertIsNotNone(self.plugin.spec.www[0].pattern)
        self.assertEqual(r"\1", self.plugin.spec.www[0].file)

        self.assertIsNone(self.plugin.spec.www[1].pattern)
        self.assertEqual("index.html", self.plugin.spec.www[1].file)

    def test_spec_menus(self):
        self.assertEqual(0, len(self.plugin.spec.menus.admin))
        self.assertEqual(0, len(self.plugin.spec.menus.group))
        self.assertEqual(1, len(self.plugin.spec.menus.project))
        self.assertEqual(0, len(self.plugin.spec.menus.user))

        project_menu = self.plugin.spec.menus.project[0]
        self.assertEqual("mdi-image-edit", project_menu.icon)
        self.assertEqual("Labeling", project_menu.name)
        self.assertEqual("/", project_menu.path)
        self.assertEqual(2, len(project_menu.lang))
        self.assertEqual("English", project_menu.lang["en"])
        self.assertEqual("Korean", project_menu.lang["ko"])


if __name__ == "__main__":
    main()
