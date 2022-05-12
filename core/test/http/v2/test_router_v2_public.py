# -*- coding: utf-8 -*-

from asyncio import get_event_loop
from unittest import IsolatedAsyncioTestCase, main

from aiohttp.hdrs import AUTHORIZATION

from recc.http import http_urls as u
from recc.http.header.basic_auth import BasicAuth
from recc.http.http_utils import v2_public_path
from recc.packet.user import SignupQ
from recc.util.version import version_text
from tester.http.http_app_tester import HttpAppTester


class RouterV2PublicTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()
        await self.tester.wait_startup()

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_heartbeat(self):
        response = await self.tester.get(v2_public_path(u.heartbeat))
        self.assertEqual(200, response.status)

    async def test_version(self):
        response = await self.tester.get(v2_public_path(u.version))
        self.assertEqual(200, response.status)
        self.assertEqual(version_text, response.data)

    async def test_state_already(self):
        response = await self.tester.get(v2_public_path(u.state_already))
        self.assertEqual(200, response.status)
        self.assertFalse(response.data)

    async def test_admin_signin(self):
        await self.tester.signup_and_in_default_admin()

    async def test_signup_and_signin(self):
        self.assertFalse(self.tester.context.config.public_signup)
        signup = SignupQ("user1", SignupQ.encrypt_password("1234"), "Nick")
        response1 = await self.tester.post(v2_public_path(u.signup), data=signup)
        self.assertEqual(503, response1.status)

        self.tester.context.config.public_signup = True
        response2 = await self.tester.post(v2_public_path(u.signup), data=signup)
        self.assertEqual(200, response2.status)

        auth = BasicAuth(signup.username, signup.password)
        signin_headers = {str(AUTHORIZATION): auth.encode()}
        response3 = await self.tester.post(
            v2_public_path(u.signin),
            headers=signin_headers,
        )
        self.assertEqual(200, response3.status)


if __name__ == "__main__":
    main()
