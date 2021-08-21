# -*- coding: utf-8 -*-

from unittest import main
from typing import List
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.http_utils import v2_path
from recc.http import http_urls as u
from recc.http import http_path_keys as p
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


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
        slug1 = "group1"
        description1 = "description1"
        features1 = ["1", "2"]
        visibility1 = VISIBILITY_LEVEL_PRIVATE
        group1 = CreateGroupQ(
            slug=slug1,
            description=description1,
            features=features1,
            visibility=visibility1,
        )
        response1 = await self.tester.post(v2_path(u.self_groups), data=group1)
        self.assertEqual(200, response1.status)
        self.assertIsNone(response1.data)

        response2 = await self.tester.get(v2_path(u.self_groups), cls=List[GroupA])
        self.assertEqual(200, response2.status)
        self.assertIsNotNone(response2.data)
        self.assertIsInstance(response2.data, list)
        self.assertEqual(1, len(response2.data))
        response2_data0 = response2.data[0]
        self.assertIsInstance(response2_data0, GroupA)
        self.assertEqual(slug1, response2_data0.slug)
        self.assertEqual(description1, response2_data0.description)
        self.assertEqual(features1, response2_data0.features)
        self.assertEqual(visibility1, response2_data0.visibility)

        path = v2_path(u.self_groups_pgroup, **{p.group: slug1})
        response3 = await self.tester.get(path, cls=GroupA)
        self.assertEqual(200, response3.status)
        self.assertIsNotNone(response3.data)
        response3_data = response3.data
        self.assertIsInstance(response3_data, GroupA)
        self.assertEqual(group1.slug, response3_data.slug)
        self.assertEqual(group1.description, response3_data.description)
        self.assertEqual(group1.features, response3_data.features)
        self.assertEqual(group1.visibility, response3_data.visibility)

        update_group1 = UpdateGroupQ(description="description2")
        response5 = await self.tester.patch(path, data=update_group1)
        self.assertEqual(200, response5.status)

        response6 = await self.tester.get(path, cls=GroupA)
        self.assertEqual(200, response6.status)
        self.assertIsNotNone(response6.data)
        self.assertIsInstance(response6.data, GroupA)
        self.assertEqual(update_group1.description, response6.data.description)

        response7 = await self.tester.delete(path)
        self.assertEqual(200, response7.status)

        response8 = await self.tester.get(v2_path(u.self_groups), cls=List[GroupA])
        self.assertEqual(200, response8.status)
        self.assertIsNotNone(response8.data)
        self.assertIsInstance(response8.data, list)
        self.assertEqual(0, len(response8.data))

    async def test_self_projects(self):
        group1 = CreateGroupQ(slug="group1")
        response1 = await self.tester.post(v2_path(u.self_groups), data=group1)
        self.assertEqual(200, response1.status)

        project1 = CreateProjectQ(group_slug=group1.slug, project_slug="project1")
        response2 = await self.tester.post(v2_path(u.self_projects), data=project1)
        self.assertEqual(200, response2.status)

        response3 = await self.tester.get(v2_path(u.self_projects), cls=List[ProjectA])
        self.assertEqual(200, response3.status)
        response3_data = response3.data
        self.assertIsNotNone(response3_data)
        self.assertIsInstance(response3_data, list)
        self.assertEqual(1, len(response3_data))
        response3_data0 = response3_data[0]
        self.assertIsInstance(response3_data0, ProjectA)
        self.assertEqual(project1.group_slug, response3_data0.group_slug)
        self.assertEqual(project1.project_slug, response3_data0.project_slug)
        self.assertIsNone(response3_data0.name)
        self.assertIsNone(response3_data0.description)
        self.assertIsNone(response3_data0.features)
        self.assertIsNone(response3_data0.extra)
        self.assertIsNotNone(response3_data0.created_at)
        self.assertIsNone(response3_data0.updated_at)

        path = v2_path(u.self_projects_pgroup_pproject).format(
            group=project1.group_slug, project=project1.project_slug
        )
        update = UpdateProjectQ(name="name1")
        response4 = await self.tester.patch(path, data=update)
        self.assertEqual(200, response4.status)

        response5 = await self.tester.get(path, cls=ProjectA)
        self.assertEqual(200, response5.status)
        response5_data = response5.data
        self.assertIsNotNone(response5_data)
        self.assertIsInstance(response5_data, ProjectA)
        self.assertEqual(project1.group_slug, response5_data.group_slug)
        self.assertEqual(project1.project_slug, response5_data.project_slug)
        self.assertEqual(update.name, response5_data.name)

        response6 = await self.tester.delete(path)
        self.assertEqual(200, response6.status)

        response7 = await self.tester.get(v2_path(u.self_projects), cls=List[ProjectA])
        self.assertEqual(200, response7.status)
        response7_data = response7.data
        self.assertIsNotNone(response7_data)
        self.assertIsInstance(response7_data, list)
        self.assertEqual(0, len(response7_data))


if __name__ == "__main__":
    main()
