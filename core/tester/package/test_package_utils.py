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
        self.assertIn("setuptools", filter_module_names("setup"))
        self.assertNotIn(
            "setuptools",
            filter_module_names("setup", denies=[r".*tool.*"]),
        )
        self.assertNotIn(
            "setuptools",
            filter_module_names("setup", allows=[r"NO_ANY"]),
        )


if __name__ == "__main__":
    main()
