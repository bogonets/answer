# -*- coding: utf-8 -*-

import os
import unittest
import json
import hashlib
from recc.http.http_app_tester import HttpAppTester
from recc.http.v1 import path_v1 as pv1
from recc.http.v1.common import k_user, get_v1_path
from recc.util.version import version_text
from tester import AsyncTestCase


def _get_test_data(filename: str) -> str:
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
    with open(data_path, "r") as f:
        return f.read()


class RouterV1TestCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()

    async def tearDown(self):
        await self.tester.teardown()

    async def test_ver(self):
        core_response = await self.tester.get_request(get_v1_path(pv1.get_core_version))
        self.assertEqual(200, core_response.status)
        core_version = core_response.data["result"]["obj"]["info"]
        self.assertEqual(version_text, core_version)

        api_response = await self.tester.get_request(get_v1_path(pv1.get_api_version))
        self.assertEqual(200, api_response.status)
        api_version = api_response.data["result"]["obj"]["info"]
        self.assertEqual(version_text, api_version)

    async def test_admin_login(self):
        await self.tester.run_v1_admin_login()
        test_login_response = await self.tester.get_request(get_v1_path(pv1.test_login))
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

        user_exist_no = await self.tester.get_request(get_v1_path(path_exist_user_my))
        self.assertEqual(200, user_exist_no.status)
        self.assertFalse(user_exist_no.data["result"]["obj"]["findId"])

        users = await self.tester.get_request(get_v1_path(pv1.get_users))
        self.assertEqual(200, users.status)
        self.assertEqual(1, len(users.data["result"]["obj"]))
        self.assertEqual("admin", users.data["result"]["obj"][0]["id"])

        user_add = await self.tester.post_request(
            get_v1_path(pv1.add_user),
            data=json.dumps({"id": username, "password": hashed_pw}),
        )
        self.assertEqual(200, user_add.status)
        self.assertEqual("OK", user_add.data["status"])

        user_exist_yes = await self.tester.get_request(get_v1_path(path_exist_user_my))
        self.assertEqual(200, user_exist_yes.status)
        self.assertTrue(user_exist_yes.data["result"]["obj"]["findId"])

        user_set_data = {"id": username, "email": email, "telephone": phone}
        user_set = await self.tester.put_request(
            get_v1_path(pv1.set_user),
            data=json.dumps(user_set_data),
        )
        self.assertEqual(200, user_set.status)
        self.assertEqual("OK", user_set.data["status"])

        user_get = await self.tester.get_request(get_v1_path(path_get_user_my))
        self.assertEqual(200, user_get.status)
        self.assertEqual(email, user_get.data["result"]["obj"]["email"])
        self.assertEqual(phone, user_get.data["result"]["obj"]["telephone"])

        user_del = await self.tester.delete_request(
            get_v1_path(pv1.delete_user),
            data=json.dumps({"id": username}),
        )
        self.assertEqual(200, user_del.status)
        self.assertEqual("OK", user_del.data["status"])

        user_exist_no_2 = await self.tester.get_request(get_v1_path(path_exist_user_my))
        self.assertEqual(200, user_exist_no_2.status)
        self.assertFalse(user_exist_no_2.data["result"]["obj"]["findId"])

    async def test_get_templates(self):
        await self.tester.run_v1_admin_login()

        templates = await self.tester.get_request(get_v1_path(pv1.get_templates))
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

    # async def test_set_graph(self):
    #     # Task: cv2.imread -> cv2.cvtColor -> cv2.imwrite
    #     graph_json_v1_data = _get_test_data("set_graph.v1.data.json")
    #     graph_json_v1_dict = json.loads(graph_json_v1_data)
    #     self.assertIsInstance(graph_json_v1_dict, dict)
    #     self.assertIn("links", graph_json_v1_dict)
    #     self.assertIn("nodes", graph_json_v1_dict)
    #     self.assertIn("tasks", graph_json_v1_dict)
    #
    #     project_name = "project1"
    #     await self.tester.run_v1_admin_login()
    #     await self.tester.post_request(
    #         get_v1_path(pv1.create_project).format(proj=project_name)
    #     )
    #
    #     set_graph = await self.tester.post_request(
    #         get_v1_path(pv1.set_proj_graph).format(proj=project_name),
    #         data=graph_json_v1_data,
    #     )
    #     self.assertEqual(200, set_graph.status)
    #     self.assertEqual("OK", set_graph.data["status"])


if __name__ == "__main__":
    unittest.main()
