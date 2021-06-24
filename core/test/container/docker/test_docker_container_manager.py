# -*- coding: utf-8 -*-

import unittest
import tempfile
from io import BytesIO
from tarfile import open as tar_open
from recc.container.container_manager_interface import ContainerStatus
from recc.container.docker.docker_container_manager import DockerContainerManager
from recc.variables.orchestration import BASE_IMAGE_FULLNAME
from recc.archive.tar_archive import file_info
from recc.util.version import parse_semantic_version
from tester import AsyncTestCase


class DockerContainerManagerTestCase(AsyncTestCase):
    async def setUp(self):
        self.cm = DockerContainerManager()
        await self.cm.open()
        self.assertTrue(self.cm.is_open())
        if not await self.cm.exist_default_task_images():
            print("Pulling default node image ...")
            await self.cm.pull_default_task_images()
            print("Pulling done.")
        self.assertTrue(await self.cm.exist_default_task_images())

    async def tearDown(self):
        await self.cm.close()

    async def test_inside_container(self):
        result = DockerContainerManager.inside_container()
        self.assertIsInstance(result, bool)
        print(f"Inside Container? {result}")

    async def test_version(self):
        docker_version_text = await self.cm.version("Version")
        docker_version = parse_semantic_version(docker_version_text)
        self.assertLessEqual(19, docker_version[0])

        api_version_text = await self.cm.version("ApiVersion")
        api_version = parse_semantic_version(api_version_text)
        self.assertLessEqual(1, api_version[0])
        self.assertLessEqual(40, api_version[1])

        min_api_version_text = await self.cm.version("MinAPIVersion")
        min_api_version = parse_semantic_version(min_api_version_text)
        self.assertLessEqual(1, min_api_version[0])
        self.assertLessEqual(12, min_api_version[1])

    async def test_build_image(self):
        container_name = "test-build-container:latest"
        file_object = BytesIO()
        dockerfile_path = "/Dockerfile"
        dockerfile = f"""From {BASE_IMAGE_FULLNAME}\nENTRYPOINT ["python", "-V"]"""
        dockerfile_bytes = dockerfile.encode("utf-8")
        with tar_open(fileobj=file_object, mode="w") as tar:
            tar.addfile(
                file_info(
                    dockerfile_path,
                    len(dockerfile_bytes),
                    0o544,
                ),
                BytesIO(dockerfile_bytes),
            )
            tar_bytes = file_object.getvalue()

        try:
            print(f"Build the '{container_name}' image ...")
            build_log = await self.cm.build_image(
                tar_bytes, container_name, "/", dockerfile_path
            )
            print(build_log)
        finally:
            if container_name in await self.cm.images():
                await self.cm.remove_image(container_name)
        self.assertTrue(len(build_log) >= 1)

    async def test_volumes(self):
        volume_key = ""
        volume_name = "test-volume-name"
        try:
            volume = await self.cm.create_volume(volume_name)
            volume_key = volume.key
            self.assertEqual(volume_name, volume.name)
            self.assertTrue(await self.cm.exist_volume(volume_key))
            await self.cm.remove_volume(volume_key)
            self.assertFalse(await self.cm.exist_volume(volume_key))
        finally:
            if await self.cm.exist_volume(volume_key):
                await self.cm.remove_volume(volume_key)

    async def test_networks(self):
        network_key = ""
        network_name = "test-network-name"
        try:
            network = await self.cm.create_network(network_name)
            network_key = network.key
            self.assertEqual(network_name, network.name)
            self.assertTrue(await self.cm.exist_network(network_key))
            await self.cm.remove_network(network_key)
            self.assertFalse(await self.cm.exist_network(network_key))
        finally:
            if await self.cm.exist_network(network_key):
                await self.cm.remove_network(network_key)

    async def test_create_task(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            container_key = ""
            group_name = "Tester"
            project_name = "MyProj"
            task_name = "recc-test-async-docker"
            rpc_bind = "[::]"
            rpc_port = 21000
            try:
                container = await self.cm.create_task(
                    group_name,
                    project_name,
                    task_name,
                    rpc_bind,
                    rpc_port,
                    workspace_volume=temp_dir,
                )
                container_key = container.key
                self.assertTrue(await self.cm.exist_container(container_key))
                nodes1 = await self.cm.get_tasks()
                self.assertLess(0, len(nodes1))
                self.assertEqual(container_key, nodes1[0].key)
                self.assertEqual(ContainerStatus.Created, nodes1[0].status)

                await self.cm.start_container(container_key)
                nodes2 = await self.cm.get_tasks(group_name, project_name, task_name)
                self.assertLess(0, len(nodes2))
                self.assertEqual(container_key, nodes2[0].key)
                self.assertEqual(ContainerStatus.Running, nodes2[0].status)

                nodes3 = await self.cm.get_task(group_name, project_name, task_name)
                self.assertEqual(container_key, nodes3.key)
                self.assertEqual(ContainerStatus.Running, nodes3.status)

                logs = await self.cm.logs_container(container_key)
                self.assertIsNotNone(logs)

                await self.cm.stop_container(container_key, timeout=1)
                nodes3 = await self.cm.get_tasks(group_name, project_name, task_name)
                self.assertLess(0, len(nodes3))
                self.assertEqual(container_key, nodes3[0].key)
                self.assertEqual(ContainerStatus.Exited, nodes3[0].status)

                await self.cm.remove_container(container_key)
            finally:
                if await self.cm.exist_container(container_key):
                    await self.cm.remove_container(container_key, force=True)


if __name__ == "__main__":
    unittest.main()
