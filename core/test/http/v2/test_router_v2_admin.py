# -*- coding: utf-8 -*-

from unittest import main
from typing import List
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.http_utils import v2_admin_path
from recc.http import http_urls as u
from recc.http import http_path_keys as p
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.group import GroupA, CreateGroupQ, UpdateGroupQ
from recc.packet.rule import RuleA, CreateRuleQ, UpdateRuleQ
from recc.packet.project import ProjectA, CreateProjectQ, UpdateProjectQ
from recc.packet.system import SystemOverviewA
from recc.log.logging import get_root_level
from logging import CRITICAL, DEBUG


class RouterV2AdminTestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()
        try:
            await self.tester.signup_and_in_default_admin()
        except:  # noqa
            await self.tester.teardown()

    async def tearDown(self):
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

        path = v2_admin_path(u.groups_pgroup.format(**{p.group: new_group1.slug}))
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
        self.assertIsNone(response3_data0.updated_at)

        path = v2_admin_path(u.projects_pgroup_pproject).format(
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

        response7 = await self.tester.get(v2_admin_path(u.projects), cls=List[ProjectA])
        self.assertEqual(200, response7.status)
        response7_data = response7.data
        self.assertIsNotNone(response7_data)
        self.assertIsInstance(response7_data, list)
        self.assertEqual(0, len(response7_data))

    async def test_permission(self):
        perm1 = CreateRuleQ("perm1", r_storage=True)
        response1 = await self.tester.post(v2_admin_path(u.rules), data=perm1)
        self.assertEqual(200, response1.status)

        response2 = await self.tester.get(
            v2_admin_path(u.rules),
            cls=List[RuleA],
        )
        self.assertEqual(200, response2.status)
        response2_data = response2.data
        self.assertIsNotNone(response2_data)
        self.assertIsInstance(response2_data, list)
        after_creation_num_permissions = len(response2_data)
        response2_datas = list(filter(lambda x: x.slug == perm1.slug, response2_data))
        response2_data0 = response2_datas[0]
        self.assertIsInstance(response2_data0, RuleA)
        self.assertEqual(perm1.slug, response2_data0.slug)
        self.assertIsNone(response2_data0.name)
        self.assertIsNone(response2_data0.description)
        self.assertIsNone(response2_data0.features)
        self.assertIsNone(response2_data0.extra)
        self.assertFalse(response2_data0.r_layout)
        self.assertFalse(response2_data0.w_layout)
        self.assertTrue(response2_data0.r_storage)
        self.assertFalse(response2_data0.w_storage)
        self.assertFalse(response2_data0.r_manager)
        self.assertFalse(response2_data0.w_manager)
        self.assertFalse(response2_data0.r_graph)
        self.assertFalse(response2_data0.w_graph)
        self.assertFalse(response2_data0.r_member)
        self.assertFalse(response2_data0.w_member)
        self.assertFalse(response2_data0.r_setting)
        self.assertFalse(response2_data0.w_setting)
        self.assertFalse(response2_data0.hidden)
        self.assertFalse(response2_data0.lock)
        self.assertIsNotNone(response2_data0.created_at)
        self.assertIsNone(response2_data0.updated_at)

        perm2_slug = "perm2"
        path1 = v2_admin_path(u.rules_prule).format(perm=perm1.slug)
        update = UpdateRuleQ(slug=perm2_slug, w_layout=True)
        response3 = await self.tester.patch(path1, data=update)
        self.assertEqual(200, response3.status)

        path2 = v2_admin_path(u.rules_prule).format(perm=perm2_slug)
        response4 = await self.tester.get(path2, cls=RuleA)
        self.assertEqual(200, response4.status)
        response4_data = response4.data
        self.assertIsNotNone(response4_data)
        self.assertIsInstance(response4_data, RuleA)
        self.assertEqual(update.slug, response4_data.slug)
        self.assertIsNone(response4_data.name)
        self.assertIsNone(response4_data.description)
        self.assertIsNone(response4_data.features)
        self.assertIsNone(response4_data.extra)
        self.assertFalse(response4_data.r_layout)
        self.assertTrue(response4_data.w_layout)
        self.assertTrue(response4_data.r_storage)
        self.assertFalse(response4_data.w_storage)
        self.assertFalse(response4_data.r_manager)
        self.assertFalse(response4_data.w_manager)
        self.assertFalse(response4_data.r_graph)
        self.assertFalse(response4_data.w_graph)
        self.assertFalse(response4_data.r_member)
        self.assertFalse(response4_data.w_member)
        self.assertFalse(response4_data.r_setting)
        self.assertFalse(response4_data.w_setting)
        self.assertFalse(response4_data.hidden)
        self.assertFalse(response4_data.lock)
        self.assertIsNotNone(response4_data.created_at)
        self.assertIsNotNone(response4_data.updated_at)

        response5 = await self.tester.delete(path2)
        self.assertEqual(200, response5.status)

        response6 = await self.tester.get(
            v2_admin_path(u.rules),
            cls=List[RuleA],
        )
        self.assertEqual(200, response6.status)
        response6_data = response6.data
        self.assertIsNotNone(response6_data)
        self.assertIsInstance(response6_data, list)

        expect_num_permissions = len(response6_data) + 1
        self.assertEqual(after_creation_num_permissions, expect_num_permissions)

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

        self.assertEqual(0, self.tester.context.config.verbose)
        self.assertEqual("0", verbose.value)

        body2 = UpdateConfigValueQ("True")
        path2 = v2_admin_path(u.configs_pkey.format(key=public_signup_key))
        response2 = await self.tester.patch(path2, data=body2)
        self.assertEqual(200, response2.status)

        body3 = UpdateConfigValueQ("1")
        path3 = v2_admin_path(u.configs_pkey.format(key=verbose_key))
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
        path = v2_admin_path(u.configs_pkey.format(key=key))
        response1 = await self.tester.patch(path, data=body)
        self.assertEqual(200, response1.status)

        response2 = await self.tester.get(path, cls=ConfigA)
        self.assertEqual(200, response2.status)
        self.assertIsInstance(response2.data, ConfigA)
        self.assertEqual(change_log_level, response2.data.value)
        self.assertEqual(expected_log_level, get_root_level())


if __name__ == "__main__":
    main()
