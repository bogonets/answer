# -*- coding: utf-8 -*-

import unittest
import json
import hashlib
from tester.samples.read_samples import read_sample
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.v1 import path_v1 as pv1
from recc.http.v1.common import k_user, get_v1_path
from recc.util.version import version_text


class RouterV1TestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.wait_startup()

    async def tearDown(self):
        await self.tester.teardown()

    async def test_ver(self):
        core_response = await self.tester.get(get_v1_path(pv1.get_core_version))
        self.assertEqual(200, core_response.status)
        core_version = core_response.data["result"]["obj"]["info"]
        self.assertEqual(version_text, core_version)

        api_response = await self.tester.get(get_v1_path(pv1.get_api_version))
        self.assertEqual(200, api_response.status)
        api_version = api_response.data["result"]["obj"]["info"]
        self.assertEqual(version_text, api_version)

    async def test_admin_login(self):
        await self.tester.run_v1_admin_login()
        test_login_response = await self.tester.get(get_v1_path(pv1.test_login))
        self.assertEqual(200, test_login_response.status)

    async def test_user(self):
        username = "my"
        password = "0000"
        email = "aaa@localhost.com"
        phone = "010-333-4444"
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        self.assertEqual(k_user, "usr")
        path_exist_user_my = pv1.exist_user.format(usr=username)
        path_get_user_my = pv1.get_user.format(usr=username)

        await self.tester.run_v1_admin_login()

        user_exist_no = await self.tester.get(get_v1_path(path_exist_user_my))
        self.assertEqual(200, user_exist_no.status)
        self.assertFalse(user_exist_no.data["result"]["obj"]["findId"])

        users = await self.tester.get(get_v1_path(pv1.get_users))
        self.assertEqual(200, users.status)
        self.assertEqual(1, len(users.data["result"]["obj"]))
        self.assertEqual("admin", users.data["result"]["obj"][0]["id"])

        user_add = await self.tester.post(
            get_v1_path(pv1.add_user),
            data=json.dumps({"id": username, "password": hashed_pw}),
        )
        self.assertEqual(200, user_add.status)
        self.assertEqual("OK", user_add.data["status"])

        user_exist_yes = await self.tester.get(get_v1_path(path_exist_user_my))
        self.assertEqual(200, user_exist_yes.status)
        self.assertTrue(user_exist_yes.data["result"]["obj"]["findId"])

        user_set_data = {"id": username, "email": email, "telephone": phone}
        user_set = await self.tester.put(
            get_v1_path(pv1.set_user),
            data=json.dumps(user_set_data),
        )
        self.assertEqual(200, user_set.status)
        self.assertEqual("OK", user_set.data["status"])

        user_get = await self.tester.get(get_v1_path(path_get_user_my))
        self.assertEqual(200, user_get.status)
        self.assertEqual(email, user_get.data["result"]["obj"]["email"])
        self.assertEqual(phone, user_get.data["result"]["obj"]["telephone"])

        user_del = await self.tester.delete(
            get_v1_path(pv1.delete_user),
            data=json.dumps({"id": username}),
        )
        self.assertEqual(200, user_del.status)
        self.assertEqual("OK", user_del.data["status"])

        user_exist_no_2 = await self.tester.get(get_v1_path(path_exist_user_my))
        self.assertEqual(200, user_exist_no_2.status)
        self.assertFalse(user_exist_no_2.data["result"]["obj"]["findId"])

    async def test_get_templates(self):
        await self.tester.run_v1_admin_login()

        templates = await self.tester.get(get_v1_path(pv1.get_templates))
        self.assertEqual(200, templates.status)
        obj = templates.data["result"]["obj"]
        self.assertIsInstance(obj, list)
        for template in obj:
            self.assertIn("info", template)
            self.assertIn("controls", template)
            self.assertIn("props", template)
            self.assertIsInstance(template["info"], dict)
            self.assertIsInstance(template["controls"], dict)
            self.assertIsInstance(template["props"], list)
            for prop in template["props"]:
                self.assertIsInstance(prop, dict)
                self.assertIn("valid", prop)
                self.assertIsInstance(prop["valid"], dict)

    async def test_create_project(self):
        await self.tester.run_v1_admin_login()

        proj0 = "demo"
        proj0_path = pv1.create_project.format(proj=proj0)
        proj0_result = await self.tester.post(get_v1_path(proj0_path))
        self.assertEqual(200, proj0_result.status)

        result = await self.tester.get(get_v1_path(pv1.get_projects))
        self.assertEqual(200, result.status)
        projects = result.data["result"]["obj"]
        self.assertIsInstance(projects, list)
        self.assertEqual(1, len(projects))
        self.assertIsInstance(projects[0], dict)
        self.assertEqual(proj0, projects[0]["name"])

    async def test_create_task_and_validation(self):
        await self.tester.run_v1_admin_login()

        proj0 = "__demo__"
        proj0_path = pv1.create_project.format(proj=proj0)
        proj0_result = await self.tester.post(get_v1_path(proj0_path))
        self.assertEqual(200, proj0_result.status)

        set_proj_graph_path = pv1.set_proj_graph.format(proj=proj0)
        set_proj_graph_request_data = read_sample("set_graph.numpy2.json")
        set_proj_graph_result = await self.tester.post(
            get_v1_path(set_proj_graph_path), data=set_proj_graph_request_data
        )
        self.assertEqual(200, set_proj_graph_result.status)

        get_proj_graph_path = pv1.get_proj_graph.format(proj=proj0)
        get_proj_graph_result = await self.tester.get(
            get_v1_path(get_proj_graph_path)
        )
        self.assertEqual(200, get_proj_graph_result.status)

        get_proj_graph_status_path = pv1.get_proj_graph_status.format(proj=proj0)
        get_proj_graph_status_result = await self.tester.get(
            get_v1_path(get_proj_graph_status_path)
        )
        self.assertEqual(200, get_proj_graph_status_result.status)

        stop_proj_task_path = pv1.stop_proj_task.format(proj=proj0, task="Task")
        result = await self.tester.post(get_v1_path(stop_proj_task_path))
        self.assertEqual(200, result.status)


if __name__ == "__main__":
    unittest.main()
