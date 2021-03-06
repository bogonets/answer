# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, main
from asyncio import get_event_loop
from tester.http.http_app_tester import HttpAppTester
from recc.http import http_urls as u
from recc.util.version import version_text


class HttpAppTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_heartbeat(self):
        result = await self.tester.get(u.api_heartbeat)
        self.assertEqual(200, result.status)

    async def test_version(self):
        result = await self.tester.get(u.api_version)
        self.assertEqual(200, result.status)
        self.assertEqual(version_text, result.data)


if __name__ == "__main__":
    main()
