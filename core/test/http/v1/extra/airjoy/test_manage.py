# -*- coding: utf-8 -*-

import json
import unittest
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.v1.common import get_airjoy_v1_path
from recc.http.v1.extra.airjoy_v1 import (
    path_get_manage_data_metric,
    path_get_manage_data_non_metric,
    path_post_manage_data_non_metric,
    path_post_manage_data_metric,
)


class AirjoyV1TestManageCase(AsyncTestCase):
    async def setUp(self):
        self.tester = HttpAppTester(self.loop)
        await self.tester.setup()
        await self.tester.run_v1_admin_login()

    async def tearDown(self):
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

        metric = await self.tester.get(
            get_airjoy_v1_path(path_get_manage_data_metric.format(proj="test"))
        )
        self.assertEqual(200, metric.status)
        self.assertEqual("OK", metric.data["status"])

        non_metric = await self.tester.get(
            get_airjoy_v1_path(path_get_manage_data_non_metric.format(proj="test")),
        )
        self.assertEqual(200, non_metric.status)
        self.assertEqual("OK", non_metric.data["status"])

        non_metric_post_data = {
            "serial": "serial1",
            "editData": ["install_date", "0406"],
        }
        non_metric_post = await self.tester.post(
            get_airjoy_v1_path(path_post_manage_data_non_metric.format(proj="test")),
            data=json.dumps(non_metric_post_data),
        )
        self.assertEqual(200, non_metric_post.status)
        self.assertEqual("OK", non_metric_post.data["status"])

        metric_post_data = {"serial": "serial1", "editData": ["firmware_version", "v3"]}
        metric_post = await self.tester.post(
            get_airjoy_v1_path(path_post_manage_data_metric.format(proj="test")),
            data=json.dumps(metric_post_data),
        )
        self.assertEqual(200, metric_post.status)
        self.assertEqual("OK", metric_post.data["status"])


if __name__ == "__main__":
    unittest.main()
