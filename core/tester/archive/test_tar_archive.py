# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from unittest import TestCase, main

from recc import archive
from recc.archive.tar_archive import compress_tar


class TarArchiveTestCase(TestCase):
    def test_compress(self):
        prefix = "prefix/path/node"
        node_init_path = os.path.abspath(archive.__file__)
        node_dir = os.path.abspath(os.path.dirname(node_init_path))
        node_data = compress_tar(node_dir, mode="w", archive_name=prefix)
        self.assertLess(0, len(node_data))
        self.assertIsInstance(node_data, bytes)

        rpc_files = [os.path.basename(archive.tar_archive.__file__)]

        with tar_open(fileobj=BytesIO(node_data), mode="r") as tar:
            names = tar.getnames()
            self.assertIn(f"{prefix}", names)
            self.assertIn(f"{prefix}/__init__.py", names)
            for f in rpc_files:
                self.assertIn(f"{prefix}/{f}", names)


if __name__ == "__main__":
    main()
