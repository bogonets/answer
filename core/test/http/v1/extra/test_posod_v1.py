# -*- coding: utf-8 -*-

import unittest
from tester.http.http_app_tester import HttpAppTester
from recc.http.v1.common import get_posod_v1_path
from tester import AsyncTestCase


class PosodV1TestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.run_v1_admin_login()

    async def tearDown(self):
        await self.tester.teardown()

    async def test_posod(self):
        result = await self.tester.get_request(get_posod_v1_path("/test"))
        self.assertEqual(200, result.status)
        self.assertEqual("OK", result.data["status"])


if __name__ == "__main__":
    unittest.main()
