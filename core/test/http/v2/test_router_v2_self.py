# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, main
from asyncio import get_event_loop
from tester.http.http_app_tester import HttpAppTester
from recc.http.http_utils import v2_self_path
from recc.http import http_urls as u
from recc.packet.user import UserExtraA


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

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_self(self):
        response = await self.tester.get(v2_self_path(u.root))
        self.assertEqual(200, response.status)
        self.assertIn("username", response.data)

    async def test_self_unknown_extra(self):
        response = await self.tester.get(v2_self_path(u.extra))
        self.assertEqual(200, response.status)
        self.assertIsNone(response.data)

        # First Handshake.
        data = {"unknown": 0, "test": "aaa"}
        response = await self.tester.patch(v2_self_path(u.extra), data=data)
        self.assertEqual(200, response.status)

        response2 = await self.tester.get(v2_self_path(u.extra))
        self.assertEqual(200, response2.status)
        self.assertEqual(data, response2.data)

        # Second Handshake.
        data2 = {"bbb": "ccc", "ddd": "eee"}
        response3 = await self.tester.patch(v2_self_path(u.extra), data=data2)
        self.assertEqual(200, response3.status)

        response4 = await self.tester.get(v2_self_path(u.extra))
        self.assertEqual(200, response4.status)
        self.assertEqual(data2, response4.data)

    async def test_self_extra(self):
        data = UserExtraA(dark=True, lang="ko")
        response = await self.tester.patch(v2_self_path(u.extra), data=data)
        self.assertEqual(200, response.status)

        response2 = await self.tester.get(v2_self_path(u.extra), cls=UserExtraA)
        self.assertEqual(200, response2.status)
        self.assertIsInstance(response2.data, UserExtraA)
        self.assertEqual(data.dark, response2.data.dark)
        self.assertEqual(data.lang, response2.data.lang)


if __name__ == "__main__":
    main()
