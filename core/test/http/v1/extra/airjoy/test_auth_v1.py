# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, main
from asyncio import get_event_loop
from tester.http.http_app_tester import HttpAppTester
from recc.http.v1.common import get_airjoy_v1_path
from recc.http.v1.extra.airjoy_v1 import (
    path_get_project_ids,
    path_get_project_members,
    path_add_project_member,
    path_edit_project_member_auth,
    path_delete_project_member,
)


class AirjoyV1TestAuthCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tester = HttpAppTester(get_event_loop())
        await self.tester.setup()
        await self.tester.run_v1_admin_login()

    async def asyncTearDown(self):
        await self.tester.teardown()

    async def test_default(self):
        result = await self.tester.get(get_airjoy_v1_path("/test"))
        self.assertEqual(200, result.status)
        self.assertEqual("OK", result.data["status"])

    async def test_airjoy(self):
        # Create Project, First Test Only
        # create_project = self.tester.post_request(
        #     get_airjoy_v1_path(get_airjoy_v1_path.create_project.format(proj="test")),
        # )
        # self.assertEqual(200, create_project.status)
        # self.assertEqual("OK", create_project.data["status"])

        project_ids_get = await self.tester.get(
            get_airjoy_v1_path(path_get_project_ids.format(proj="test")),
        )
        self.assertEqual(200, project_ids_get.status)
        self.assertEqual("OK", project_ids_get.data["status"])

        project_members_get = await self.tester.get(
            get_airjoy_v1_path(path_get_project_members.format(proj="test")),
        )
        self.assertEqual(200, project_members_get.status)
        self.assertEqual("OK", project_members_get.data["status"])

        project_member_add = await self.tester.post(
            get_airjoy_v1_path(path_add_project_member.format(proj="test")),
        )
        self.assertEqual(200, project_member_add.status)
        self.assertEqual("OK", project_member_add.data["status"])

        project_member_auth_edit = await self.tester.post(
            get_airjoy_v1_path(path_edit_project_member_auth.format(proj="test")),
        )
        self.assertEqual(200, project_member_auth_edit.status)
        self.assertEqual("OK", project_member_auth_edit.data["status"])

        project_member_delete = await self.tester.post(
            get_airjoy_v1_path(path_delete_project_member.format(proj="test")),
        )
        self.assertEqual(200, project_member_delete.status)
        self.assertEqual("OK", project_member_delete.data["status"])


if __name__ == "__main__":
    main()
