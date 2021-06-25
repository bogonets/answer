# -*- coding: utf-8 -*-

from unittest import main
from io import BytesIO
from tarfile import open as tar_open
from recc.variables.container import BASE_IMAGE_FULLNAME
from recc.archive.tar_archive import file_info
from tester import DockerTestCase


class DockerImageTestCase(DockerTestCase):
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
            build_log = await self.container.build_image(
                tar_bytes, container_name, "/", dockerfile_path
            )
            print(build_log)
        finally:
            if container_name in await self.container.images():
                await self.container.remove_image(container_name)
        self.assertTrue(len(build_log) >= 1)


if __name__ == "__main__":
    main()
