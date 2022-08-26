# -*- coding: utf-8 -*-

from asyncio import get_event_loop
from unittest import IsolatedAsyncioTestCase, main

from recc.http import http_urls as u
from recc.http.http_utils import v2_self_path
from tester.http.http_app_tester import HttpAppTester


class RouterV2SelfTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()
        await self.tester.wait_startup()

        self.username = "user1"
        self.password = "1234"
        try:
            await self.tester.signup_default_admin()
            await self.tester.signup(self.username, self.password)
            await self.tester.signin(self.username, self.password, save_session=True)
        except:  # noqa
            await self.tester.teardown()
            raise

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_self(self):
        response = await self.tester.get(v2_self_path(u.root))
        self.assertEqual(200, response.status)
        self.assertIn("username", response.data)


if __name__ == "__main__":
    main()
