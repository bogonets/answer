# -*- coding: utf-8 -*-

import unittest
from recc.http.http_app_tester import HttpAppTester
from recc.http.http_vars import URL_API_HEARTBEAT, URL_API_VERSION
from recc.util.version import version_text
from tester import AsyncTestCase


class HttpAppTestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()

    async def tearDown(self):
        await self.tester.teardown()

    async def test_heartbeat(self):
        result = await self.tester.get_request(URL_API_HEARTBEAT)
        self.assertEqual(200, result.status)

    async def test_version(self):
        result = await self.tester.get_request(URL_API_VERSION)
        self.assertEqual(200, result.status)
        self.assertEqual(version_text, result.data)


if __name__ == "__main__":
    unittest.main()
