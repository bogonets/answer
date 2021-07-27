# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http import http_urls as u
from recc.http.http_utils import v2_path


class RouterV1TestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()

    async def tearDown(self):
        await self.tester.teardown()

    async def test_admin_login(self):
        await self.tester.run_v2_admin_login()
        self_response = await self.tester.get(v2_path(u.self))
        self.assertEqual(200, self_response.status)
        self.assertIn("username", self_response.data)


if __name__ == "__main__":
    main()
