# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from recc.package.recc_package import extract_recc_module


class TarArchiveTestCase(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    def test_extract_recc_module(self):
        extract_recc_module(self.temp.name)
        recc_dir = os.path.join(self.temp.name, "recc")
        recc_init_py = os.path.join(recc_dir, "__init__.py")
        self.assertTrue(os.path.isdir(recc_dir))
        self.assertTrue(os.path.isfile(recc_init_py))


if __name__ == "__main__":
    main()
