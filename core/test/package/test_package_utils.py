# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main
from recc.package.package_utils import (
    get_module_directory,
    get_recc_module_directory,
    list_submodule_names,
    all_module_names,
    find_module_names,
)
from recc import lamda_builtin


class PackageUtilsTestCase(TestCase):
    def test_get_recc_module_directory(self):
        self.assertTrue(os.path.isdir(get_recc_module_directory()))

    def test_get_module_directory(self):
        self.assertTrue(os.path.isdir(get_module_directory(lamda_builtin)))

    def test_list_submodule_names(self):
        self.assertIn("numpy", list_submodule_names(lamda_builtin))

    def test_all_module_names(self):
        self.assertIn("pip", all_module_names())
        self.assertIn("setuptools", all_module_names())

    def test_find_module_names(self):
        self.assertIn("setuptools", find_module_names("setup"))


if __name__ == "__main__":
    main()
