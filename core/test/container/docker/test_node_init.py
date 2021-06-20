# -*- coding: utf-8 -*-

import os
from io import BytesIO
from unittest import TestCase
from unittest import main as unittest_main
from tarfile import open as tar_open
from recc.container.docker.node_init import (
    RECC_MODULE_INIT_PATH,
    RECC_MODULE_DIR,
    COMPRESS_NODE_INIT_TAR_BYTES,
)
from recc.archive.tar_archive import remove_first_slash
from recc.variables.task_guest import TASK_GUEST_ROOT_DIR, TASK_GUEST_PACKAGE_DIR


class NodeInitTestCase(TestCase):
    def test_vars(self):
        self.assertTrue(os.path.isdir(RECC_MODULE_DIR))
        self.assertEqual("__init__.py", os.path.basename(RECC_MODULE_INIT_PATH))

    def test_node_init_tar(self):
        io_bytes = BytesIO(COMPRESS_NODE_INIT_TAR_BYTES)
        with tar_open(fileobj=io_bytes, mode="r") as tar:
            tar_names = [f.name for f in tar]
            self.assertIn(remove_first_slash(TASK_GUEST_ROOT_DIR), tar_names)
            self.assertIn(remove_first_slash(TASK_GUEST_PACKAGE_DIR), tar_names)


if __name__ == "__main__":
    unittest_main()
