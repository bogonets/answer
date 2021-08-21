# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.http_utils import v2_path
from recc.http import http_urls as u

# from typing import List
# from recc.variables.database import RECC_DB_VERSION_KEY
# from recc.http import http_path_keys as p
# from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
# from recc.packet.info import InfoA, CreateInfoQ
# from recc.packet.permission import PermissionA, CreatePermissionQ, UpdatePermissionQ
# from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
# from recc.packet.system import SystemOverviewA
# from recc.packet.user import SignupQ


class RouterV2SelfTestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()

        self.username = "user1"
        self.password = "1234"
        await self.tester.signup_default_admin()
        await self.tester.signup(self.username, self.password)
        await self.tester.signin(self.username, self.password, save_session=True)

    async def tearDown(self):
        await self.tester.teardown()

    async def test_self(self):
        response = await self.tester.get(v2_path(u.self))
        self.assertEqual(200, response.status)
        self.assertIn("username", response.data)

    async def test_self_extra(self):
        response = await self.tester.get(v2_path(u.self_extra))
        self.assertEqual(200, response.status)
        self.assertIsNone(response.data)

        # First Handshake.
        data = {"unknown": 0, "test": "aaa"}
        response = await self.tester.patch(v2_path(u.self_extra), data=data)
        self.assertEqual(200, response.status)

        response2 = await self.tester.get(v2_path(u.self_extra))
        self.assertEqual(200, response2.status)
        self.assertEqual(data, response2.data)

        # Second Handshake.
        data2 = {"bbb": "ccc", "ddd": "eee"}
        response3 = await self.tester.patch(v2_path(u.self_extra), data=data2)
        self.assertEqual(200, response3.status)

        response4 = await self.tester.get(v2_path(u.self_extra))
        self.assertEqual(200, response4.status)
        self.assertEqual(data2, response4.data)

    async def test_self_groups(self):
        response = await self.tester.get(v2_path(u.self_groups))
        self.assertEqual(200, response.status)


if __name__ == "__main__":
    main()
