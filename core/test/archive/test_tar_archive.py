# -*- coding: utf-8 -*-

import os
import unittest
import tarfile
import io
from recc import rpc
from recc.rpc import async_rpc_client
from recc.rpc import async_rpc_client_manager
from recc.rpc import async_rpc_server
from recc.archive.tar_archive import compress_tar


class TarArchiveTestCase(unittest.TestCase):
    def test_compress(self):
        prefix = "prefix/path/node"
        node_init_path = os.path.abspath(rpc.__file__)
        node_dir = os.path.abspath(os.path.dirname(node_init_path))
        node_data = compress_tar(node_dir, mode="w", archive_name=prefix)
        self.assertLess(0, len(node_data))
        self.assertIsInstance(node_data, bytes)

        rpc_files = (
            os.path.basename(async_rpc_client.__file__),
            os.path.basename(async_rpc_client_manager.__file__),
            os.path.basename(async_rpc_server.__file__),
        )

        with tarfile.open(fileobj=io.BytesIO(node_data), mode="r") as tar:
            names = tar.getnames()
            self.assertIn(f"{prefix}", names)
            self.assertIn(f"{prefix}/__init__.py", names)
            for f in rpc_files:
                self.assertIn(f"{prefix}/{f}", names)


if __name__ == "__main__":
    unittest.main()
