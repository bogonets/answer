# -*- coding: utf-8 -*-

import unittest
import tempfile
from recc.container.container_manager_interface import ContainerStatus
from recc.container.docker.docker_container_manager import DockerContainerManager
from recc.util.version import parse_semantic_version
from tester import AsyncTestCase


class DockerContainerManagerTestCase(AsyncTestCase):
    async def setUp(self):
        self.container = DockerContainerManager()
        await self.container.open()
        self.assertTrue(self.container.is_open())
        if not await self.container.exist_default_task_images():
            print("Pulling default node image ...")
            await self.container.pull_default_task_images()
            print("Pulling done.")
        self.assertTrue(await self.container.exist_default_task_images())

    async def tearDown(self):
        await self.container.close()

    async def test_inside_container(self):
        result = DockerContainerManager.inside_container()
        self.assertIsInstance(result, bool)
        print(f"Inside Container? {result}")

    async def test_version(self):
        docker_version_text = await self.container.version("Version")
        docker_version = parse_semantic_version(docker_version_text)
        self.assertLessEqual(19, docker_version[0])

        api_version_text = await self.container.version("ApiVersion")
        api_version = parse_semantic_version(api_version_text)
        self.assertLessEqual(1, api_version[0])
        self.assertLessEqual(40, api_version[1])

        min_api_version_text = await self.container.version("MinAPIVersion")
        min_api_version = parse_semantic_version(min_api_version_text)
        self.assertLessEqual(1, min_api_version[0])
        self.assertLessEqual(12, min_api_version[1])

    async def test_volumes(self):
        volume_key = ""
        volume_name = "test-volume-name"
        try:
            volume = await self.container.create_volume(volume_name)
            volume_key = volume.key
            self.assertEqual(volume_name, volume.name)
            self.assertTrue(await self.container.exist_volume(volume_key))
            await self.container.remove_volume(volume_key)
            self.assertFalse(await self.container.exist_volume(volume_key))
        finally:
            if await self.container.exist_volume(volume_key):
                await self.container.remove_volume(volume_key)

    async def test_networks(self):
        network_key = ""
        network_name = "test-network-name"
        try:
            network = await self.container.create_network(network_name)
            network_key = network.key
            self.assertEqual(network_name, network.name)
            self.assertTrue(await self.container.exist_network(network_key))
            await self.container.remove_network(network_key)
            self.assertFalse(await self.container.exist_network(network_key))
        finally:
            if await self.container.exist_network(network_key):
                await self.container.remove_network(network_key)

    async def test_create_task(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            container_key = ""
            group_name = "Tester"
            project_name = "MyProj"
            task_name = "recc-test-async-docker"
            rpc_bind = "[::]"
            rpc_port = 21000
            try:
                container = await self.container.create_task(
                    group_name,
                    project_name,
                    task_name,
                    rpc_bind,
                    rpc_port,
                    workspace_volume=temp_dir,
                )
                container_key = container.key
                self.assertTrue(await self.container.exist_container(container_key))
                nodes1 = await self.container.get_tasks()
                self.assertLess(0, len(nodes1))
                self.assertEqual(container_key, nodes1[0].key)
                self.assertEqual(ContainerStatus.Created, nodes1[0].status)

                await self.container.start_container(container_key)
                nodes2 = await self.container.get_tasks(
                    group_name, project_name, task_name
                )
                self.assertLess(0, len(nodes2))
                self.assertEqual(container_key, nodes2[0].key)
                self.assertEqual(ContainerStatus.Running, nodes2[0].status)

                nodes3 = await self.container.get_task(
                    group_name, project_name, task_name
                )
                self.assertEqual(container_key, nodes3.key)
                self.assertEqual(ContainerStatus.Running, nodes3.status)

                logs = await self.container.logs_container(container_key)
                self.assertIsNotNone(logs)

                await self.container.stop_container(container_key, timeout=1)
                nodes3 = await self.container.get_tasks(
                    group_name, project_name, task_name
                )
                self.assertLess(0, len(nodes3))
                self.assertEqual(container_key, nodes3[0].key)
                self.assertEqual(ContainerStatus.Exited, nodes3[0].status)

                await self.container.remove_container(container_key)
            finally:
                if await self.container.exist_container(container_key):
                    await self.container.remove_container(container_key, force=True)


if __name__ == "__main__":
    unittest.main()
