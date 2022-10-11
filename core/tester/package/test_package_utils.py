# -*- coding: utf-8 -*-

import os
from importlib import import_module
from unittest import TestCase, main

from recc import package
from recc.package.package_utils import (
    all_module_names,
    filter_module_names,
    get_module_directory,
    list_submodule_names,
)


class PackageUtilsTestCase(TestCase):
    def test_get_recc_module_directory(self):
        recc_module_directory = get_module_directory(import_module("recc"))
        self.assertTrue(os.path.isdir(recc_module_directory))

    def test_get_module_directory(self):
        self.assertTrue(os.path.isdir(get_module_directory(package)))

    def test_list_submodule_names(self):
        self.assertIn("package_utils", list_submodule_names(package))

    def test_all_module_names(self):
        self.assertIn("pip", all_module_names())
        self.assertIn("setuptools", all_module_names())

    def test_filter_module_names(self):
        names1 = filter_module_names(prefix="setup")
        self.assertIn("setuptools", names1)

        names2 = filter_module_names("setup", denies=[r".*tool.*"])
        self.assertNotIn("setuptools", names2)

        names3 = filter_module_names("setup", allows=[r"NO_ANY"])
        self.assertNotIn("setuptools", names3)


if __name__ == "__main__":
    main()
