# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.core.struct.signup import Signup
from recc.http import http_urls as u
from recc.http.header.basic_auth import BasicAuth
from recc.http.http_utils import v2_public_path
from recc.util.version import version_text
from aiohttp.hdrs import AUTHORIZATION


class RouterV2PublicTestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()

    async def tearDown(self):
        await self.tester.teardown()

    async def test_heartbeat(self):
        response = await self.tester.get(v2_public_path(u.heartbeat))
        self.assertEqual(200, response.status)

    async def test_version(self):
        response = await self.tester.get(v2_public_path(u.version))
        self.assertEqual(200, response.status)
        self.assertEqual(version_text, response.data)

    async def test_test_init(self):
        response = await self.tester.get(v2_public_path(u.test_init))
        self.assertEqual(503, response.status)

    async def test_admin_signin(self):
        await self.tester.run_v2_admin_signin()

    async def test_signup_and_signin(self):
        self.assertFalse(self.tester.context.config.public_signup)
        signup = Signup("user1", Signup.encrypt_password("1234"), "Nick")
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
