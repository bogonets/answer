# -*- coding: utf-8 -*-

from unittest import main
from typing import List
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.http_utils import v2_main_path
from recc.http import http_urls as u
from recc.http import http_path_keys as p
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
from recc.packet.member import MemberA, CreateMemberQ, UpdateMemberQ
from recc.packet.permission import PermissionA
from recc.packet.info import InfoA
from recc.variables.database import (
    VISIBILITY_LEVEL_PRIVATE,
    PERMISSION_NAME_GUEST,
    PERMISSION_NAME_REPORTER,
    PERMISSION_NAME_OWNER,
    PERMISSION_NAMES,
)


class RouterV2MainTestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()

        self.username = "main1"
        self.password = "1234"
        await self.tester.signup_default_admin()
        await self.tester.signup(self.username, self.password)
        await self.tester.signin(self.username, self.password, save_session=True)

    async def tearDown(self):
        await self.tester.teardown()

    async def test_groups(self):
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
        response1 = await self.tester.post(v2_main_path(u.groups), data=group1)
        self.assertEqual(200, response1.status)
        self.assertIsNone(response1.data)

        response2 = await self.tester.get(v2_main_path(u.groups), cls=List[GroupA])
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

        path = v2_main_path(u.groups_pgroup, **{p.group: slug1})
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

        response8 = await self.tester.get(v2_main_path(u.groups), cls=List[GroupA])
        self.assertEqual(200, response8.status)
        self.assertIsNotNone(response8.data)
        self.assertIsInstance(response8.data, list)
        self.assertEqual(0, len(response8.data))

    async def test_group_members(self):
        another_username = "another1"
        another_password = "12345678"
        await self.tester.signup(another_username, another_password)

        slug1 = "group1"
        group1 = CreateGroupQ(slug=slug1)
        response1 = await self.tester.post(v2_main_path(u.groups), data=group1)
        self.assertEqual(200, response1.status)

        path1 = v2_main_path(u.groups_pgroup_members, group=slug1)
        response2 = await self.tester.get(path1, cls=List[MemberA])
        self.assertEqual(200, response2.status)
        response2_data = response2.data
        self.assertIsInstance(response2_data, list)
        self.assertEqual(1, len(response2_data))
        response2_data0 = response2_data[0]
        self.assertIsInstance(response2_data0, MemberA)
        self.assertEqual(self.username, response2_data0.username)
        self.assertEqual(PERMISSION_NAME_OWNER, response2_data0.permission)

        member1 = CreateMemberQ(another_username, PERMISSION_NAME_REPORTER)
        response3 = await self.tester.post(path1, data=member1)
        self.assertEqual(200, response3.status)

        response4 = await self.tester.get(path1, cls=List[MemberA])
        self.assertEqual(200, response4.status)
        self.assertEqual(2, len(response4.data))

        path2 = v2_main_path(
            u.groups_pgroup_members_pmember, group=slug1, member=another_username
        )
        response5 = await self.tester.get(path2, cls=MemberA)
        self.assertEqual(200, response5.status)
        response5_data = response5.data
        self.assertIsInstance(response5_data, MemberA)
        self.assertEqual(another_username, response5_data.username)
        self.assertEqual(PERMISSION_NAME_REPORTER, response5_data.permission)

        update1 = UpdateMemberQ(another_username, PERMISSION_NAME_GUEST)
        response6 = await self.tester.patch(path2, data=update1)
        self.assertEqual(200, response6.status)

        response7 = await self.tester.get(path2, cls=MemberA)
        self.assertEqual(200, response7.status)
        response7_data = response7.data
        self.assertIsInstance(response7_data, MemberA)
        self.assertEqual(another_username, response7_data.username)
        self.assertEqual(PERMISSION_NAME_GUEST, response7_data.permission)

        response8 = await self.tester.delete(path2)
        self.assertEqual(200, response8.status)

        response9 = await self.tester.get(path1, cls=List[MemberA])
        self.assertEqual(200, response9.status)
        self.assertEqual(1, len(response9.data))

    async def test_group_projects(self):
        group1 = CreateGroupQ(slug="group1")
        group2 = CreateGroupQ(slug="group2")
        response1 = await self.tester.post(v2_main_path(u.groups), data=group1)
        response2 = await self.tester.post(v2_main_path(u.groups), data=group2)
        self.assertEqual(200, response1.status)
        self.assertEqual(200, response2.status)

        project1 = CreateProjectQ(group_slug=group1.slug, project_slug="project1")
        project2 = CreateProjectQ(group_slug=group2.slug, project_slug="project2")
        response3 = await self.tester.post(v2_main_path(u.projects), data=project1)
        response4 = await self.tester.post(v2_main_path(u.projects), data=project2)
        self.assertEqual(200, response3.status)
        self.assertEqual(200, response4.status)

        path1 = v2_main_path(u.groups_pgroup_projects, group=group1.slug)
        path2 = v2_main_path(u.groups_pgroup_projects, group=group2.slug)
        response5 = await self.tester.get(path1, cls=List[ProjectA])
        response6 = await self.tester.get(path2, cls=List[ProjectA])
        self.assertEqual(200, response5.status)
        self.assertEqual(200, response6.status)

        self.assertEqual(1, len(response5.data))
        self.assertEqual(1, len(response6.data))
        response5_data0 = response5.data[0]
        response6_data0 = response6.data[0]
        self.assertIsInstance(response5_data0, ProjectA)
        self.assertIsInstance(response6_data0, ProjectA)
        self.assertEqual(project1.project_slug, response5_data0.project_slug)
        self.assertEqual(project2.project_slug, response6_data0.project_slug)

    async def test_projects(self):
        group1 = CreateGroupQ(slug="group1")
        response1 = await self.tester.post(v2_main_path(u.groups), data=group1)
        self.assertEqual(200, response1.status)

        project1 = CreateProjectQ(group_slug=group1.slug, project_slug="project1")
        response2 = await self.tester.post(v2_main_path(u.projects), data=project1)
        self.assertEqual(200, response2.status)

        response3 = await self.tester.get(v2_main_path(u.projects), cls=List[ProjectA])
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

        path = v2_main_path(u.projects_pgroup_pproject).format(
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

        response7 = await self.tester.get(v2_main_path(u.projects), cls=List[ProjectA])
        self.assertEqual(200, response7.status)
        response7_data = response7.data
        self.assertIsNotNone(response7_data)
        self.assertIsInstance(response7_data, list)
        self.assertEqual(0, len(response7_data))

    async def test_project_members(self):
        another_username = "another1"
        another_password = "12345678"
        await self.tester.signup(another_username, another_password)

        group1 = CreateGroupQ(slug="group1")
        response1 = await self.tester.post(v2_main_path(u.groups), data=group1)
        self.assertEqual(200, response1.status)

        project1 = CreateProjectQ(group_slug=group1.slug, project_slug="project1")
        response2 = await self.tester.post(v2_main_path(u.projects), data=project1)
        self.assertEqual(200, response2.status)

        path1 = v2_main_path(
            u.projects_pgroup_pproject_members,
            group=project1.group_slug,
            project=project1.project_slug,
        )
        response3 = await self.tester.get(path1, cls=List[MemberA])
        self.assertEqual(200, response3.status)
        response3_data = response3.data
        self.assertIsInstance(response3_data, list)
        self.assertEqual(1, len(response3_data))
        response3_data0 = response3_data[0]
        self.assertIsInstance(response3_data0, MemberA)
        self.assertEqual(self.username, response3_data0.username)
        self.assertEqual(PERMISSION_NAME_OWNER, response3_data0.permission)

        member1 = CreateMemberQ(another_username, PERMISSION_NAME_REPORTER)
        response4 = await self.tester.post(path1, data=member1)
        self.assertEqual(200, response4.status)

        response5 = await self.tester.get(path1, cls=List[MemberA])
        self.assertEqual(200, response5.status)
        self.assertEqual(2, len(response5.data))

        path2 = v2_main_path(
            u.projects_pgroup_pproject_members_pmember,
            group=project1.group_slug,
            project=project1.project_slug,
            member=another_username,
        )
        response6 = await self.tester.get(path2, cls=MemberA)
        self.assertEqual(200, response6.status)
        response6_data = response6.data
        self.assertIsInstance(response6_data, MemberA)
        self.assertEqual(another_username, response6_data.username)
        self.assertEqual(PERMISSION_NAME_REPORTER, response6_data.permission)

        update1 = UpdateMemberQ(another_username, PERMISSION_NAME_GUEST)
        response7 = await self.tester.patch(path2, data=update1)
        self.assertEqual(200, response7.status)

        response8 = await self.tester.get(path2, cls=MemberA)
        self.assertEqual(200, response8.status)
        response8_data = response8.data
        self.assertIsInstance(response8_data, MemberA)
        self.assertEqual(another_username, response8_data.username)
        self.assertEqual(PERMISSION_NAME_GUEST, response8_data.permission)

        response9 = await self.tester.delete(path2)
        self.assertEqual(200, response9.status)

        response10 = await self.tester.get(path1, cls=List[MemberA])
        self.assertEqual(200, response10.status)
        self.assertEqual(1, len(response10.data))

    async def test_permissions(self):
        response1 = await self.tester.get(v2_main_path(u.permissions))
        self.assertEqual(200, response1.status)
        response1_data = response1.data
        self.assertIsInstance(response1_data, list)
        self.assertEqual(len(PERMISSION_NAMES), len(response1_data))

    async def test_group_and_project_permissions(self):
        group1 = CreateGroupQ(slug="group1")
        response1 = await self.tester.post(v2_main_path(u.groups), data=group1)
        self.assertEqual(200, response1.status)

        project1 = CreateProjectQ(group_slug=group1.slug, project_slug="project1")
        response2 = await self.tester.post(v2_main_path(u.projects), data=project1)
        self.assertEqual(200, response2.status)

        path1 = v2_main_path(u.permissions_pgroup, group=group1.slug)
        response3 = await self.tester.get(path1, cls=PermissionA)
        self.assertEqual(200, response3.status)
        response3_data = response3.data
        self.assertIsInstance(response3_data, PermissionA)
        self.assertEqual(PERMISSION_NAME_OWNER, response3_data.name)

        path2 = v2_main_path(
            u.permissions_pgroup_pproject,
            group=project1.group_slug,
            project=project1.project_slug,
        )
        response4 = await self.tester.get(path2, cls=PermissionA)
        self.assertEqual(200, response4.status)
        response4_data = response4.data
        self.assertIsInstance(response4_data, PermissionA)
        self.assertEqual(PERMISSION_NAME_OWNER, response4_data.name)

    async def test_usernames(self):
        user1_username = "user1"
        user1_password = "11111"
        await self.tester.signup(user1_username, user1_password)

        user2_username = "user2"
        user2_password = "22222"
        await self.tester.signup(user2_username, user2_password)

        response1 = await self.tester.get(v2_main_path(u.usernames), cls=List[str])
        self.assertEqual(200, response1.status)
        response1_data = response1.data
        self.assertIsInstance(response1_data, list)
        self.assertIn(self.username, response1_data)
        self.assertIn(user1_username, response1_data)
        self.assertIn(user2_username, response1_data)

    async def test_infos_oem(self):
        response1 = await self.tester.get(v2_main_path(u.infos_oem))
        self.assertNotEqual(200, response1.status)

        oem = "tester"
        await self.tester.context.set_info_oem(oem)

        response2 = await self.tester.get(v2_main_path(u.infos_oem), cls=InfoA)
        self.assertEqual(200, response2.status)
        response2_data = response2.data
        self.assertIsInstance(response2_data, InfoA)
        self.assertEqual(oem, response2_data.value)


if __name__ == "__main__":
    main()
