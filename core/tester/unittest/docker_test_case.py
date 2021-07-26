# -*- coding: utf-8 -*-

from tester.unittest.async_test_case import AsyncTestCase
from recc.container.docker.docker_container_manager import DockerContainerManager


class DockerTestCase(AsyncTestCase):
    async def setUp(self):
        self.container = DockerContainerManager()
        await self.container.open()
        self.assertTrue(self.container.is_open())

    async def tearDown(self):
        self.assertTrue(self.container.is_open())
        await self.container.close()
        self.assertFalse(self.container.is_open())
