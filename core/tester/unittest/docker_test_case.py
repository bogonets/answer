# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase

from recc.container.docker.docker_container_manager import DockerContainerManager


class DockerTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.container = DockerContainerManager()
        await self.container.open()
        self.assertTrue(self.container.is_open())

    async def asyncTearDown(self):
        self.assertTrue(self.container.is_open())
        await self.container.close()
        self.assertFalse(self.container.is_open())
