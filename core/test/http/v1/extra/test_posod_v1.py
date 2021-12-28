# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, main
from asyncio import get_event_loop
from tester.http.http_app_tester import HttpAppTester
from recc.http.v1.common import get_posod_v1_path


class PosodV1TestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()
        await self.tester.run_v1_admin_login()

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_posod(self):
        result = await self.tester.get(get_posod_v1_path("/test"))
        self.assertEqual(200, result.status)
        self.assertEqual("OK", result.data["status"])


if __name__ == "__main__":
    main()
