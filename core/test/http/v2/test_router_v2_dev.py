# -*- coding: utf-8 -*-

from asyncio import get_event_loop
from typing import List
from unittest import IsolatedAsyncioTestCase, main

from recc.http import http_path_keys as p
from recc.http import http_urls as u
from recc.http.http_utils import v2_dev_path
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.info import CreateInfoQ, InfoA
from recc.packet.plugin import PluginA
from recc.variables.database import INFO_KEY_RECC_DB_VERSION
from tester.http.http_app_tester import HttpAppTester


class RouterV2DevTestCase(IsolatedAsyncioTestCase):
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

    async def test_infos(self):
        response1 = await self.tester.get(v2_dev_path(u.infos), cls=List[InfoA])
        self.assertEqual(200, response1.status)
        self.assertIsInstance(response1.data, list)
        version = list(
            filter(lambda x: x.key == INFO_KEY_RECC_DB_VERSION, response1.data)
        )
        self.assertEqual(1, len(version))
        self.assertEqual(INFO_KEY_RECC_DB_VERSION, version[0].key)

        info1 = CreateInfoQ("key1", "value2")
        response2 = await self.tester.post(v2_dev_path(u.infos), data=info1)
        self.assertEqual(200, response2.status)
        self.assertIsNone(response2.data)

        path = v2_dev_path(u.infos_pkey.format_map({p.key: info1.key}))
        response3 = await self.tester.get(path)
        self.assertEqual(200, response3.status)
        self.assertIsNotNone(response3.data)

        response4 = await self.tester.delete(path)
        self.assertEqual(200, response4.status)

        response5 = await self.tester.get(path)
        self.assertNotEqual(200, response5.status)

    async def test_plugins(self):
        path = v2_dev_path(u.plugins)
        response = await self.tester.get(path, cls=List[PluginA])
        self.assertEqual(200, response.status)
        self.assertIsNotNone(response.data)
        self.assertIsInstance(response.data, list)

    async def test_configs(self):
        path1 = v2_dev_path(u.configs)
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
        path2 = v2_dev_path(u.configs_pkey.format_map({p.key: public_signup_key}))
        response2 = await self.tester.patch(path2, data=body2)
        self.assertEqual(200, response2.status)

        body3 = UpdateConfigValueQ("1")
        path3 = v2_dev_path(u.configs_pkey.format_map({p.key: verbose_key}))
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


if __name__ == "__main__":
    main()
