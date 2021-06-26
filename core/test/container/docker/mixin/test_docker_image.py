# -*- coding: utf-8 -*-

from unittest import main
from io import BytesIO
from tarfile import open as tar_open
from recc.variables.container import BASE_IMAGE_FULLNAME
from recc.archive.tar_archive import file_info
from tester import DockerTestCase

TEST_CONTAINER_NAME = "recc-test-build-image:latest"
TEST_DOCKERFILE_PATH = "/Dockerfile"
DOCKERFILE_CONTENT = f"""
From {BASE_IMAGE_FULLNAME}
ENTRYPOINT ["python", "-V"]
"""
DOCKERFILE_CONTENT_BYTES = DOCKERFILE_CONTENT.encode("utf-8")


class DockerImageTestCase(DockerTestCase):
    async def test_build_image(self):
        container_name = TEST_CONTAINER_NAME
        dockerfile_path = TEST_DOCKERFILE_PATH
        dockerfile_bytes = DOCKERFILE_CONTENT_BYTES
        dockerfile_info = file_info(dockerfile_path, len(dockerfile_bytes), 0o544)
        dockerfile_io = BytesIO(DOCKERFILE_CONTENT_BYTES)

        file_object = BytesIO()
        with tar_open(fileobj=file_object, mode="w") as tar:
            tar.addfile(dockerfile_info, dockerfile_io)
            tar_bytes = file_object.getvalue()

        try:
            print(f"Building docker image: {container_name} ...")
            build_log = await self.container.build_image(
                tar_bytes, container_name, "/", dockerfile_path
            )
            if build_log:
                print(f"Build message: {build_log}")
            else:
                print("Empty build message")
        finally:
            if container_name in await self.container.images():
                await self.container.remove_image(container_name)


if __name__ == "__main__":
    main()
