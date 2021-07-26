# -*- coding: utf-8 -*-

import unittest
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
# from recc.http import http_urls as u
# from recc.http.http_utils import v2_public_path


class RouterV1TestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()

    async def tearDown(self):
        await self.tester.teardown()

    # web.get(u.heartbeat, self.get_heartbeat),
    # web.get(u.version, self.get_version),
    # web.get(u.test_init, self.get_test_init),
    # web.post(u.signup_admin, self.post_signup_admin),
    # web.post(u.signup, self.post_signup),
    # web.post(u.login, self.post_login),
    #
    # async def test_version(self):
    #     v2_public_path(u.version)
    #     core_response = await self.tester.get_request(v2_public_path(u.version))
    #     self.assertEqual(200, core_response.status)
    #     core_version = core_response.data["result"]["obj"]["info"]
    #     self.assertEqual(version_text, core_version)
    #
    #     api_response = await self.tester.get_request(get_v1_path(pv1.get_api_version))
    #     self.assertEqual(200, api_response.status)
    #     api_version = api_response.data["result"]["obj"]["info"]
    #     self.assertEqual(version_text, api_version)


if __name__ == "__main__":
    unittest.main()
