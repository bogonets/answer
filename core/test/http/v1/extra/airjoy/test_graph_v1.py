# -*- coding: utf-8 -*-

import json
import unittest
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.http.v1.common import get_airjoy_v1_path
from recc.http.v1.extra.airjoy_v1 import (
    path_get_agency_list,
    path_get_graph_term,
    path_get_graph_live,
    path_post_manage_device_signal,
)


class AirjoyV1TestGraphCase(AsyncTestCase):
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

        agency_list = await self.tester.get(
            get_airjoy_v1_path(path_get_agency_list.format(proj="test")),
        )
        self.assertEqual(200, agency_list.status)
        self.assertEqual("OK", agency_list.data["status"])
        expected_agency_list = [
            {"id": 1, "name": "agency1"},
            {"id": 2, "name": "agency2"},
            {"id": 3, "name": "agency3"},
        ]
        self.assertEqual(expected_agency_list, agency_list.data["result"])

        graph_term_data = {"agency": "agency1", "start": "", "end": ""}
        graph_term = await self.tester.post(
            get_airjoy_v1_path(path_get_graph_term.format(proj="test")),
            data=json.dumps(graph_term_data),
        )
        self.assertEqual(200, graph_term.status)
        self.assertEqual("OK", graph_term.data["status"])

        graph_live = await self.tester.get(
            get_airjoy_v1_path(
                path_get_graph_live.format(proj="test", agency="agency1")
            ),
        )
        self.assertEqual(200, graph_live.status)
        self.assertEqual("OK", graph_live.data["status"])

        device_signal_data = {"serial": "serial1", "device": "on_off"}
        device_signal = await self.tester.post(
            get_airjoy_v1_path(path_post_manage_device_signal.format(proj="test")),
            data=json.dumps(device_signal_data),
        )
        self.assertEqual(200, device_signal.status)
        self.assertEqual("OK", device_signal.data["status"])


if __name__ == "__main__":
    unittest.main()
