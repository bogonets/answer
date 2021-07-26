# -*- coding: utf-8 -*-

import unittest
from tester.http.http_app_tester import HttpAppTester
from recc.http import http_urls as u
from recc.util.version import version_text
from tester import AsyncTestCase


class HttpAppTestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()

    async def tearDown(self):
        await self.tester.teardown()

    async def test_heartbeat(self):
        result = await self.tester.get_request(u.api_heartbeat)
        self.assertEqual(200, result.status)

    async def test_version(self):
        result = await self.tester.get_request(u.api_version)
        self.assertEqual(200, result.status)
        self.assertEqual(version_text, result.data)


if __name__ == "__main__":
    unittest.main()
