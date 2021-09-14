# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.http_utils import v2_plugins_path
from recc.http import http_urls as u


class RouterV2PluginsTestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()

        self.username = "user1"
        self.password = "1234"
        await self.tester.signup_default_admin()
        await self.tester.signup(self.username, self.password)
        await self.tester.signin(self.username, self.password, save_session=True)

    async def tearDown(self):
        await self.tester.teardown()

    async def test_root(self):
        response = await self.tester.get(v2_plugins_path(u.root))
        self.assertEqual(200, response.status)


if __name__ == "__main__":
    main()
