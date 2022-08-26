# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from unittest import TestCase, main

from recc.archive.tar_archive import remove_first_slash
from recc.container.docker.task_init import (
    BUILD_CONTEXT_DOCKERFILE_PATH,
    BUILD_CONTEXT_RECC_PATH,
    get_compressed_task_dockerfile_tar,
)
from recc.package.recc_package import RECC_MODULE_DIR, RECC_MODULE_INIT_PATH


class TaskInitTestCase(TestCase):
    def test_vars(self):
        self.assertTrue(os.path.isdir(RECC_MODULE_DIR))
        self.assertEqual("__init__.py", os.path.basename(RECC_MODULE_INIT_PATH))

    def test_get_compressed_task_dockerfile_tar(self):
        context_tar = get_compressed_task_dockerfile_tar()
        io_bytes = BytesIO(context_tar)
        with tar_open(fileobj=io_bytes, mode="r") as tar:
            tar_names = [f.name for f in tar]
            dockerfile = remove_first_slash(BUILD_CONTEXT_DOCKERFILE_PATH)
            self.assertIn(dockerfile, tar_names)

            recc = remove_first_slash(BUILD_CONTEXT_RECC_PATH)
            self.assertIn(recc, tar_names)


if __name__ == "__main__":
    main()
