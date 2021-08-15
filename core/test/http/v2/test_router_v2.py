# -*- coding: utf-8 -*-

from unittest import main
from typing import List
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.variables.database import RECC_DB_VERSION_KEY
from recc.http.http_utils import v2_path
from recc.http import http_urls as u
from recc.http import http_path_keys as p
from recc.packet.update_info import UpdateInfoQ
from recc.packet.system_overview import SystemOverviewA
from recc.database.struct.info import Info
from recc.database.struct.group import Group


class RouterV2TestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()
        await self.tester.run_v2_admin_signin()

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

    async def test_infos(self):
        response1 = await self.tester.get(v2_path(u.infos), cls=List[Info])
        self.assertEqual(200, response1.status)
        self.assertIsInstance(response1.data, list)
        version = list(filter(lambda x: x.key == RECC_DB_VERSION_KEY, response1.data))
        self.assertEqual(1, len(version))
        self.assertEqual(RECC_DB_VERSION_KEY, version[0].key)

        update_info = UpdateInfoQ("key1", "value2")
        response2 = await self.tester.post(v2_path(u.infos), data=update_info)
        self.assertEqual(200, response2.status)
        self.assertIsNone(response2.data)

        path = v2_path(u.infos_pkey.format(**{p.key: update_info.key}))
        response3 = await self.tester.get(path)
        self.assertEqual(200, response3.status)
        self.assertIsNotNone(response3.data)

        response4 = await self.tester.delete(path)
        self.assertEqual(200, response4.status)

        response5 = await self.tester.get(path)
        self.assertNotEqual(200, response5.status)

    async def test_users(self):
        response = await self.tester.get(v2_path(u.users))
        self.assertEqual(200, response.status)
        self.assertIsNotNone(response.data)

    async def test_groups(self):
        response = await self.tester.get(v2_path(u.groups), cls=List[Group])
        self.assertEqual(200, response.status)
        self.assertIsNotNone(response.data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(1, len(response.data))  # Anonymous group
        response_data0 = response.data[0]
        self.assertIsInstance(response_data0, Group)
        anonymous_slug = response_data0.slug

        new_group1 = Group(
            slug="group1",
            description="description1",
            features=["1", "2"],
        )
        response2 = await self.tester.post(v2_path(u.groups), data=new_group1)
        self.assertEqual(200, response2.status)
        self.assertIsNone(response2.data)

        response3 = await self.tester.get(v2_path(u.groups), cls=List[Group])
        self.assertEqual(200, response3.status)
        self.assertIsNotNone(response3.data)
        self.assertIsInstance(response3.data, list)
        self.assertEqual(2, len(response3.data))
        group1 = list(filter(lambda g: g.slug != anonymous_slug, response3.data))[0]
        self.assertIsInstance(group1, Group)
        self.assertEqual(new_group1.slug, group1.slug)
        self.assertEqual(new_group1.description, group1.description)
        self.assertEqual(new_group1.features, group1.features)

        path = v2_path(u.groups_pgroup.format(**{p.group: new_group1.slug}))
        response4 = await self.tester.get(path, cls=Group)
        self.assertEqual(200, response4.status)
        self.assertIsNotNone(response4.data)
        self.assertIsInstance(response4.data, Group)
        self.assertEqual(new_group1.slug, response4.data.slug)
        self.assertEqual(new_group1.description, response4.data.description)
        self.assertEqual(new_group1.features, response4.data.features)

        update_group1 = Group(description="description2")
        response5 = await self.tester.patch(path, data=update_group1)
        self.assertEqual(200, response5.status)

        response6 = await self.tester.get(path, cls=Group)
        self.assertEqual(200, response6.status)
        self.assertIsNotNone(response6.data)
        self.assertIsInstance(response6.data, Group)
        self.assertEqual(update_group1.description, response6.data.description)

        response7 = await self.tester.delete(path)
        self.assertEqual(200, response7.status)

        response8 = await self.tester.get(v2_path(u.groups), cls=List[Group])
        self.assertEqual(200, response8.status)
        self.assertIsNotNone(response8.data)
        self.assertIsInstance(response8.data, list)
        self.assertEqual(1, len(response8.data))  # Anonymous group

    async def test_system_overview(self):
        path = v2_path(u.system_overview)
        response = await self.tester.get(path, cls=SystemOverviewA)
        self.assertEqual(200, response.status)
        self.assertIsNotNone(response.data)
        self.assertIsInstance(response.data, SystemOverviewA)
        self.assertIsNotNone(response.data.users)
        self.assertIsNotNone(response.data.groups)
        self.assertIsNotNone(response.data.projects)
        self.assertLessEqual(0, response.data.users)
        self.assertLessEqual(0, response.data.groups)
        self.assertLessEqual(0, response.data.projects)


if __name__ == "__main__":
    main()
