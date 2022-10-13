# -*- coding: utf-8 -*-

from asyncio import get_event_loop
from logging import CRITICAL, DEBUG
from typing import List
from unittest import IsolatedAsyncioTestCase, main

from recc.http import http_path_keys as p
from recc.http import http_urls as u
from recc.http.http_utils import v2_admin_path
from recc.logging.logging import get_root_level
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.group import CreateGroupQ, GroupA, UpdateGroupQ
from recc.packet.project import CreateProjectQ, ProjectA, UpdateProjectQ
from recc.packet.role import CreateRoleQ, RoleA, UpdateRoleQ
from recc.packet.system import SystemOverviewA
from recc.variables.database import (
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
)
from tester.http.http_app_tester import HttpAppTester


class RouterV2AdminTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()
        await self.tester.wait_startup()
        try:
            await self.tester.signup_and_in_default_admin()
        except:  # noqa
            await self.tester.teardown()
            raise

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_users(self):
        response = await self.tester.get(v2_admin_path(u.users))
        self.assertEqual(200, response.status)
        self.assertIsNotNone(response.data)

    async def test_groups(self):
        response = await self.tester.get(v2_admin_path(u.groups), cls=List[GroupA])
        self.assertEqual(200, response.status)
        self.assertIsNotNone(response.data)
        self.assertIsInstance(response.data, list)
        self.assertEqual(0, len(response.data))

        new_group1 = CreateGroupQ(
            slug="group1",
            description="description1",
            features=["1", "2"],
        )
        response2 = await self.tester.post(v2_admin_path(u.groups), data=new_group1)
        self.assertEqual(200, response2.status)
        self.assertIsNone(response2.data)

        response3 = await self.tester.get(v2_admin_path(u.groups), cls=List[GroupA])
        self.assertEqual(200, response3.status)
        self.assertIsNotNone(response3.data)
        self.assertIsInstance(response3.data, list)
        self.assertEqual(1, len(response3.data))
        group1 = response3.data[0]
        self.assertIsInstance(group1, GroupA)
        self.assertEqual(new_group1.slug, group1.slug)
        self.assertEqual(new_group1.description, group1.description)
        self.assertEqual(new_group1.features, group1.features)

        path = v2_admin_path(u.groups_pgroup.format_map({p.group: new_group1.slug}))
        response4 = await self.tester.get(path, cls=GroupA)
        self.assertEqual(200, response4.status)
        self.assertIsNotNone(response4.data)
        self.assertIsInstance(response4.data, GroupA)
        self.assertEqual(new_group1.slug, response4.data.slug)
        self.assertEqual(new_group1.description, response4.data.description)
        self.assertEqual(new_group1.features, response4.data.features)

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

        response8 = await self.tester.get(v2_admin_path(u.groups), cls=List[GroupA])
        self.assertEqual(200, response8.status)
        self.assertIsNotNone(response8.data)
        self.assertIsInstance(response8.data, list)
        self.assertEqual(0, len(response8.data))

    async def test_projects(self):
        group1 = CreateGroupQ(slug="group1")
        response1 = await self.tester.post(v2_admin_path(u.groups), data=group1)
        self.assertEqual(200, response1.status)

        project1 = CreateProjectQ(group_slug=group1.slug, project_slug="project1")
        response2 = await self.tester.post(v2_admin_path(u.projects), data=project1)
        self.assertEqual(200, response2.status)

        response3 = await self.tester.get(v2_admin_path(u.projects), cls=List[ProjectA])
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
        self.assertIsNotNone(response3_data0.updated_at)
        self.assertEqual(response3_data0.created_at, response3_data0.updated_at)

        path_suffix = u.projects_pgroup_pproject.format_map(
            {
                p.group: project1.group_slug,
                p.project: project1.project_slug,
            }
        )
        path = v2_admin_path(path_suffix)
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

        response7 = await self.tester.get(v2_admin_path(u.projects), cls=List[ProjectA])
        self.assertEqual(200, response7.status)
        response7_data = response7.data
        self.assertIsNotNone(response7_data)
        self.assertIsInstance(response7_data, list)
        self.assertEqual(0, len(response7_data))

    async def test_role(self):
        permissions1 = [
            PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
            PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
        ]
        role1 = CreateRoleQ("role1", permissions=permissions1)
        response1 = await self.tester.post(v2_admin_path(u.roles), data=role1)
        self.assertEqual(200, response1.status)

        response2 = await self.tester.get(
            v2_admin_path(u.roles),
            cls=List[RoleA],
        )
        self.assertEqual(200, response2.status)
        response2_data = response2.data
        self.assertIsNotNone(response2_data)
        self.assertIsInstance(response2_data, list)
        after_creation_num_roles = len(response2_data)
        response2_datas = list(filter(lambda x: x.slug == role1.slug, response2_data))
        response2_data0 = response2_datas[0]
        self.assertIsInstance(response2_data0, RoleA)
        self.assertEqual(role1.slug, response2_data0.slug)
        self.assertIsNone(response2_data0.name)
        self.assertIsNone(response2_data0.description)
        self.assertIsNone(response2_data0.extra)
        self.assertFalse(response2_data0.hidden)
        self.assertFalse(response2_data0.lock)
        self.assertIsNotNone(response2_data0.created_at)
        self.assertIsNotNone(response2_data0.updated_at)
        self.assertEqual(response2_data0.created_at, response2_data0.updated_at)
        sorted_permissions1 = list(set(permissions1))
        sorted_response2_permissions = list(set(response2_data0.permissions))
        self.assertListEqual(sorted_permissions1, sorted_response2_permissions)

        permissions2 = [
            PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
            PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
        ]
        role2_slug = "role2"
        path1 = v2_admin_path(u.roles_prole.format_map({p.role: role1.slug}))
        update = UpdateRoleQ(slug=role2_slug, permissions=permissions2)
        response3 = await self.tester.patch(path1, data=update)
        self.assertEqual(200, response3.status)

        path2 = v2_admin_path(u.roles_prole.format_map({p.role: role2_slug}))
        response4 = await self.tester.get(path2, cls=RoleA)
        self.assertEqual(200, response4.status)
        response4_data = response4.data
        self.assertIsNotNone(response4_data)
        self.assertIsInstance(response4_data, RoleA)
        self.assertEqual(update.slug, response4_data.slug)
        self.assertIsNone(response4_data.name)
        self.assertIsNone(response4_data.description)
        self.assertIsNone(response4_data.extra)
        self.assertFalse(response4_data.hidden)
        self.assertFalse(response4_data.lock)
        self.assertIsNotNone(response4_data.created_at)
        self.assertIsNotNone(response4_data.updated_at)
        self.assertNotEqual(response4_data.created_at, response4_data.updated_at)
        sorted_permissions2 = list(set(permissions2))
        sorted_response4_permissions = list(set(response4_data.permissions))
        self.assertListEqual(sorted_permissions2, sorted_response4_permissions)

        response5 = await self.tester.delete(path2)
        self.assertEqual(200, response5.status)

        response6 = await self.tester.get(
            v2_admin_path(u.roles),
            cls=List[RoleA],
        )
        self.assertEqual(200, response6.status)
        response6_data = response6.data
        self.assertIsNotNone(response6_data)
        self.assertIsInstance(response6_data, list)

        expect_num_roles = len(response6_data) + 1
        self.assertEqual(after_creation_num_roles, expect_num_roles)

    async def test_system_overview(self):
        path = v2_admin_path(u.system_overview)
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

    async def test_configs(self):
        path1 = v2_admin_path(u.configs)
        response1 = await self.tester.get(path1, cls=List[ConfigA])
        self.assertEqual(200, response1.status)
        self.assertIsNotNone(response1.data)
        self.assertIsInstance(response1.data, list)

        public_signup_key = "public_signup"
        verbose_key = "verbose"

        data1 = response1.data
        public_signup = list(filter(lambda x: x.key == public_signup_key, data1))[0]
        verbose = list(filter(lambda x: x.key == verbose_key, data1))[0]

        self.assertFalse(self.tester.context.config.public_signup)
        self.assertEqual("False", public_signup.value)

        self.assertEqual(2, self.tester.context.config.verbose)
        self.assertEqual("2", verbose.value)

        body2 = UpdateConfigValueQ("True")
        path2 = v2_admin_path(u.configs_pkey.format_map({p.key: public_signup_key}))
        response2 = await self.tester.patch(path2, data=body2)
        self.assertEqual(200, response2.status)

        body3 = UpdateConfigValueQ("1")
        path3 = v2_admin_path(u.configs_pkey.format_map({p.key: verbose_key}))
        response3 = await self.tester.patch(path3, data=body3)
        self.assertEqual(200, response3.status)

        response4 = await self.tester.get(path2, cls=ConfigA)
        self.assertEqual(200, response4.status)
        self.assertIsInstance(response4.data, ConfigA)
        self.assertEqual("True", response4.data.value)

        response5 = await self.tester.get(path3, cls=ConfigA)
        self.assertEqual(200, response5.status)
        self.assertIsInstance(response5.data, ConfigA)
        self.assertEqual("1", response5.data.value)

    async def test_log_level_configs(self):
        current_level = get_root_level()
        if current_level == CRITICAL:
            change_log_level = "Debug"
            expected_log_level = DEBUG
        else:
            change_log_level = "Critical"
            expected_log_level = CRITICAL

        key = "log_level"
        body = UpdateConfigValueQ(change_log_level)
        path = v2_admin_path(u.configs_pkey.format_map({p.key: key}))
        response1 = await self.tester.patch(path, data=body)
        self.assertEqual(200, response1.status)

        response2 = await self.tester.get(path, cls=ConfigA)
        self.assertEqual(200, response2.status)
        self.assertIsInstance(response2.data, ConfigA)
        self.assertEqual(change_log_level, response2.data.value)
        self.assertEqual(expected_log_level, get_root_level())


if __name__ == "__main__":
    main()
