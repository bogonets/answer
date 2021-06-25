# -*- coding: utf-8 -*-

import os
from io import BytesIO
from unittest import TestCase, main
from tarfile import open as tar_open
from recc.container.docker.task_init import (
    RECC_MODULE_INIT_PATH,
    RECC_MODULE_DIR,
    TASK_GUEST_WORKSPACE_DIR,
    TASK_GUEST_PACKAGE_DIR,
    TASK_INIT_TAR_BYTES,
)
from recc.archive.tar_archive import remove_first_slash


class TaskInitTestCase(TestCase):
    def test_vars(self):
        self.assertTrue(os.path.isdir(RECC_MODULE_DIR))
        self.assertEqual("__init__.py", os.path.basename(RECC_MODULE_INIT_PATH))

    def test_task_init_tar_bytes(self):
        io_bytes = BytesIO(TASK_INIT_TAR_BYTES)
        with tar_open(fileobj=io_bytes, mode="r") as tar:
            tar_names = [f.name for f in tar]
            self.assertIn(remove_first_slash(TASK_GUEST_WORKSPACE_DIR), tar_names)
            self.assertIn(remove_first_slash(TASK_GUEST_PACKAGE_DIR), tar_names)


if __name__ == "__main__":
    main()
