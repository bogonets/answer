# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.core.struct.signup_request import SignupRequest
from recc.http import http_urls as u
from recc.http.http_utils import v2_public_path
from recc.util.version import version_text


class RouterV1TestCase(AsyncTestCase):
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

    async def test_signup(self):
        self.assertFalse(self.tester.context.config.public_signup)
        signup = SignupRequest("user1", SignupRequest.encrypt_password("1234"), "Nick")
        response1 = await self.tester.post(v2_public_path(u.signup), data=signup)
        self.assertEqual(503, response1.status)

        self.tester.context.config.public_signup = True
        response2 = await self.tester.post(v2_public_path(u.signup), data=signup)
        self.assertEqual(200, response2.status)


if __name__ == "__main__":
    main()
