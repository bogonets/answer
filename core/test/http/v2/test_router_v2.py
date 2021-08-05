# -*- coding: utf-8 -*-

import json
from unittest import main
from tester.unittest.async_test_case import AsyncTestCase
from tester.http.http_app_tester import HttpAppTester
from recc.variables.database import RECC_DB_VERSION_KEY
from recc.http.http_utils import v2_path
from recc.http import http_urls as u
from recc.http import http_path_keys as p

from recc.database.struct.info import keys as info_keys


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
        response = await self.tester.patch(
            v2_path(u.self_extra),
            data=json.dumps(data),
        )
        self.assertEqual(200, response.status)

        response2 = await self.tester.get(v2_path(u.self_extra))
        self.assertEqual(200, response2.status)
        self.assertEqual(data, response2.data)

        # Second Handshake.
        data2 = {"bbb": "ccc", "ddd": "eee"}
        response3 = await self.tester.patch(
            v2_path(u.self_extra),
            data=json.dumps(data2),
        )
        self.assertEqual(200, response3.status)

        response4 = await self.tester.get(v2_path(u.self_extra))
        self.assertEqual(200, response4.status)
        self.assertEqual(data2, response4.data)

    async def test_infos(self):
        response1 = await self.tester.get(v2_path(u.infos))
        self.assertEqual(200, response1.status)
        self.assertIn(RECC_DB_VERSION_KEY, response1.data)

        dk = info_keys
        key = "config-key"
        value = "config-value"
        data = {dk.key: key, dk.value: value}
        response2 = await self.tester.post(v2_path(u.infos), data=json.dumps(data))
        self.assertEqual(200, response2.status)
        self.assertIsNone(response2.data)

        path = v2_path(u.infos_pkey.format(**{p.key: key}))
        response3 = await self.tester.get(path)
        self.assertEqual(200, response3.status)
        self.assertEqual(value, response3.data)

        response4 = await self.tester.delete(path)
        self.assertEqual(200, response4.status)

        response5 = await self.tester.get(path)
        self.assertNotEqual(200, response5.status)


if __name__ == "__main__":
    main()
