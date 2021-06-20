# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main
from recc.package.package_utils import get_module_directory, list_submodule_names
from recc import node_builtin


class PackageUtilsTestCase(TestCase):
    def test_get_module_directory(self):
        self.assertTrue(os.path.isdir(get_module_directory(node_builtin)))

    def test_list_submodule_names(self):
        self.assertIn("numpy", list_submodule_names(node_builtin))


if __name__ == "__main__":
    main()
